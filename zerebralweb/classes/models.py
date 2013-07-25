from django.db import models
from teachers.models import Teacher
from students.models import Student
from schools.models import School,PointCategory


# terms hold classes, the point categories, and begin/end date
class Term(models.Model):
    school = models.ForeignKey(School)
    begin_date = models.DateField()
    end_date = models.DateField()
    # all of the point categories and their weights for this term
    point_categories = models.ManyToManyField(PointCategory)

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_id = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher)
    term = models.ForeignKey(Term)