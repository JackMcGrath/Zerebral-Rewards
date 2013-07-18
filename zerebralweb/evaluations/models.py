from django.db import models
import datetime
from students.models import Student
from classes.models import Course
from schools.models import PointCategory


# there is one assessment per point category of the term
class Assessment(models.Model):
    point_category = models.ForeignKey(PointCategory)
    score = models.IntegerField()

# an evaluation recorded by the teacher for a particular class/student
class Evaluation(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    assessments = models.ManyToManyField(Assessment)
    date = models.DateField(default=datetime.date.today)