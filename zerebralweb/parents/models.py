from django.db import models
from students.models import Student

# parent
class Parent(models.Model):
    students = models.ManyToManyField(Student)