from . models import Students,Teachers
from . forms import StudentForm, TeacherForm
from django.db.models import Q
from django.contrib import messages
from django.db import models
from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView,UpdateView,DeleteView,ListView,DetailView,TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from axes.handlers.proxy import AxesProxyHandler





class StyledLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter the username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter the password"}))

class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = StyledLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Login successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        if AxesProxyHandler.is_locked(self.request, credentials={"username": form.data.get("username")}):
            messages.error(self.request, "Too many failed attempts. Please try again later.")
        else:
            messages.error(self.request, "Invalid username or password!")
        return super().form_invalid(form)





class UserLogoutView(LogoutView):
    next_page = "login_page"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == "POST":
            messages.success(request, "Logout successfully!")
        return response





class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_count"] = Students.objects.count()
        context["teacher_count"] = Teachers.objects.count()
        context["subject_count"] = Students.objects.values("subject").distinct().count()
        context["students_by_subject"] = (Students.objects.values("subject").annotate(total=models.Count("id")).order_by("subject"))
        context["teachers_by_subject"] = (Teachers.objects.values("subject").annotate(total=models.Count("id")).order_by("subject"))
        return context





class MyDetailsView(LoginRequiredMixin, TemplateView):
    template_name = "my_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Students.objects.filter(user=self.request.user).first()
        if student:
            context.update({"x": student, "type": "student"})
            return context
        teacher = Teachers.objects.filter(user=self.request.user).first()
        if teacher:
            context.update({"x": teacher, "type": "teacher"})
            return context
        context["error"] = "No profile is connected to this account"
        return context





    
class SuperuserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied

class StudentDetailView(SuperuserDetailView):
    model = Students
    template_name = "s_details.html"
    context_object_name = "x"

class TeacherDetailView(SuperuserDetailView):
    model = Teachers
    template_name = "t_details.html"
    context_object_name = "x"





class PersonListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    paginate_by = 5
    context_object_name = "person"

    def get_queryset(self):
        queryset = self.model.objects.all()

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(**{f"{self.id_field}__icontains": search}) |
                Q(subject__icontains=search) |
                Q(email__icontains=search))

        subject = self.request.GET.get("subject")
        if subject:
            queryset = queryset.filter(subject=subject.upper())

        sort = self.request.GET.get("sort")
        if sort in self.allowed_sorts:
            queryset = queryset.order_by(self.allowed_sorts[sort])
        elif sort:
            messages.error(self.request, "Invalid sorting option")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()
        return context

class StudentListView(PersonListView):
    model = Students
    template_name = "student.html"
    permission_required = "connect.view_students"
    raise_exception = True
    id_field = "student_id"
    allowed_sorts = {"id": "student_id", "date": "joined_date", "subject": "subject", "name": "name", "email": "email"}

class TeacherListView(PersonListView):
    model = Teachers
    template_name = "teacher.html"
    permission_required = "connect.view_teachers"
    raise_exception = True
    id_field = "teacher_id"
    allowed_sorts = {"id": "teacher_id", "date": "joined_date", "subject": "subject", "name": "name", "email": "email"}





class PersonFormMixin(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True
    success_message = ""

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)



class StudentCreateView(PersonFormMixin, CreateView):
    model = Students
    form_class = StudentForm
    template_name = "create_student.html"
    success_url = reverse_lazy("student_list")
    permission_required = "connect.add_students"
    success_message = "Student added successfully."

class TeacherCreateView(PersonFormMixin, CreateView):
    model = Teachers
    form_class = TeacherForm
    template_name = "create_teacher.html"
    success_url = reverse_lazy("teacher_list")
    permission_required = "connect.add_teachers"
    success_message = "Teacher added successfully."



class StudentUpdateView(PersonFormMixin, UpdateView):
    model = Students
    form_class = StudentForm
    template_name = "update_student.html"
    success_url = reverse_lazy("student_list")
    permission_required = "connect.change_students"
    success_message = "Student updated successfully."

class TeacherUpdateView(PersonFormMixin, UpdateView):
    model = Teachers
    form_class = TeacherForm
    template_name = "update_teacher.html"
    success_url = reverse_lazy("teacher_list")
    permission_required = "connect.change_teachers"
    success_message = "Teacher updated successfully."



class StudentDeleteView(PersonFormMixin, DeleteView):
    model = Students
    template_name = "delete_student.html"
    context_object_name = "person"
    success_url = reverse_lazy("student_list")
    permission_required = "connect.delete_students"
    success_message = "Student deleted successfully."

class TeacherDeleteView(PersonFormMixin, DeleteView):
    model = Teachers
    template_name = "delete_teacher.html"
    context_object_name = "person"
    success_url = reverse_lazy("teacher_list")
    permission_required = "connect.delete_teachers"
    success_message = "Teacher deleted successfully."
