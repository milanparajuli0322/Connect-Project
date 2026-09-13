from django import forms
from .models import Students,Teachers
from datetime import date



class BasePersonForm(forms.ModelForm):
    def clean_name(self):
        name=self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must contain at least 2 characters.")
        stripped = name.replace(" ", "").replace("-", "").replace("'", "")
        if not stripped.isalpha():
            raise forms.ValidationError("Name can only contain letters and spaces.")
        return name
    def clean_email(self):
        email=self.cleaned_data["email"].strip().lower()
        return email
    
    def clean_joined_date(self):
        joined_date=self.cleaned_data["joined_date"]
        if joined_date>date.today():
            raise forms.ValidationError("Joined date cannot be in the future.")
        return joined_date
    
    def clean_subject(self):
        subject = self.cleaned_data["subject"].strip().upper()
        allowed_subjects = ["SOFTWARE ENGINEERING","CYBERSECURITY","ARTIFICIAL INTELLIGENCE",]
        if subject not in allowed_subjects:
            raise forms.ValidationError("Select a valid subject.")
        return subject



class StudentForm(BasePersonForm):
    class Meta:
        model = Students
        fields = ["name", "student_id", "subject", "joined_date", "email"]
        widgets = {"joined_date": forms.DateInput(attrs={"type": "date"}),}
        error_messages={"student_id":{"unique":"This student id is already registered."}}

    def clean_student_id(self):
        student_id=self.cleaned_data["student_id"]
        if student_id<10000:
            raise forms.ValidationError("Student ID must contain at least 5 digits.")
        if student_id>99999:
            raise forms.ValidationError( "Student ID cannot exceed 5 digits.")
        return student_id



class TeacherForm(BasePersonForm):
    class Meta:
        model = Teachers
        fields = ["name", "teacher_id", "subject", "joined_date", "email"]
        widgets = {"joined_date": forms.DateInput(attrs={"type": "date"}),}
        error_messages={"teacher_id":{"unique":"This teacher id is already registered."}}

    def clean_teacher_id(self):
        teacher_id=self.cleaned_data["teacher_id"]
        if teacher_id<10000:
            raise forms.ValidationError("Teacher ID must contain at least 5 digits.")
        if teacher_id>99999:
            raise forms.ValidationError( "Teacher ID cannot exceed 5 digits.")
        return teacher_id
