from django.urls import path
from . import views



urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name="login_page"),
    path('logout/',views.UserLogoutView.as_view(),name='logout_page'),

    path('home/',views.HomeView.as_view(),name="home_page"),
    path('home/about/',views.AboutView.as_view(),name="about_page"),

    path('home/students/',views.StudentListView.as_view(),name="student_list"),
    path('home/students/create/',views.StudentCreateView.as_view(),name="create_student"),
    path('home/students/update/<slug:slug>/',views.StudentUpdateView.as_view(),name="update_student"),
    path('home/students/delete/<slug:slug>/',views.StudentDeleteView.as_view(),name="delete_student"),

    path('home/teachers/',views.TeacherListView.as_view(),name="teacher_list"),
    path('home/teachers/create/',views.TeacherCreateView.as_view(),name="create_teacher"),
    path('home/teachers/update/<slug:slug>/',views.TeacherUpdateView.as_view(),name="update_teacher"),
    path('home/teachers/delete/<slug:slug>/',views.TeacherDeleteView.as_view(),name="delete_teacher"),

    path('home/my-details/',views.MyDetailsView.as_view(),name="my_details"),
    path('home/students/<slug:slug>/',views.StudentDetailView.as_view(),name="student_details"),
    path('home/teachers/<slug:slug>/',views.TeacherDetailView.as_view(),name="teacher_details"),
]
