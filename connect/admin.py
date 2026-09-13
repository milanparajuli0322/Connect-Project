from django.contrib import admin
from connect.models import Students,Teachers



class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "student_id")
    search_fields = ("name","student_id", "email", "subject")
    list_filter = ("subject", "joined_date")
admin.site.register(Students, StudentAdmin)



class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher_id")
    search_fields = ("name", "teacher_id", "email", "subject")
    list_filter = ("subject", "joined_date")
admin.site.register(Teachers, TeacherAdmin)
