from django.db import models
from teachers.models import Teacher
from students.models import Student
from goals.models import Goal

# each term can have any number of point categories with a specific weight
class PointCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    # whether this category can be edited by the teacher or not
    editable = models.BooleanField(default=False)
    weight = models.DecimalField(default=1.0, max_digits=15, decimal_places=2)

# terms hold classes, the point categories, and begin/end date
class Term(models.Model):
    teacher = models.ForeignKey(Teacher)
    begin_date = models.DateField()
    end_date = models.DateField()
    # all of the point categories and their weights for this term
    point_categories = models.ManyToManyField(PointCategory)

class Course(models.Model):
    name = models.CharField(max_length=100)
    goals = models.ManyToManyField(Goal)
    course_id = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher)
    term = models.ForeignKey(Term)