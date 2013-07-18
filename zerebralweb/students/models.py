from django.db import models
from schools.models import School
from badges.models import Badge

# student
class Student(models.Model):
    school = models.ForeignKey(School)
    pts_spent = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge)