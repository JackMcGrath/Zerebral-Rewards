from django.db import models
import datetime
from students.models import EnrolledStudent
from schools.models import PointCategory

# there is one assessment per point category of the term
class Assessment(models.Model):
    point_category = models.ForeignKey(PointCategory)
    score = models.IntegerField()

# an evaluation recorded by the teacher for a particular class/student
class Evaluation(models.Model):
    # there is one enrolled student per class
    student = models.ForeignKey(EnrolledStudent)

    assessments = models.ManyToManyField(Assessment)
    date = models.DateField(default=datetime.date.today)
    grade_percent = models.IntegerField()
    engagement_percent = models.IntegerField()
    note = models.CharField(max_length=500)