from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User



class Person(models.Model):
    class Subject(models.TextChoices):
        SOFTWARE_ENGINEERING = "SOFTWARE ENGINEERING", "Software Engineering"
        CYBERSECURITY = "CYBERSECURITY", "Cybersecurity"
        ARTIFICIAL_INTELLIGENCE = "ARTIFICIAL INTELLIGENCE", "Artificial Intelligence"
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=100,db_index=True)
    subject=models.CharField(max_length=50, choices=Subject.choices,db_index=True)
    joined_date=models.DateField(db_index=True)
    email=models.EmailField(max_length=255,unique=True)
    slug=models.SlugField(unique=True, blank=True)

    class Meta:
        abstract=True

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(f"{self.name}-{self.id_field()}")
        super().save(*args,**kwargs)


    
class Students(Person):
    student_id=models.IntegerField(unique=True)

    def id_field(self):
        return self.student_id

class Teachers(Person):
    teacher_id=models.IntegerField(unique=True)

    def id_field(self):
        return self.teacher_id
