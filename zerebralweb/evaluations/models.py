from django.db import models
from students.models import EnrolledStudent
from schools.models import PointCategory
from classes.models import Course

# there is one assessment per point category of the term
class Assessment(models.Model):
    point_category = models.ForeignKey(PointCategory)
    score = models.IntegerField()

    def __unicode__(self):
        return unicode(self.point_category.name)

    def __getitem__(self, key):
        if key == 'pg':
            return unicode(self.point_category.name)
        else:
            return None

# an evaluation recorded by the teacher for a particular class/student
class Evaluation(models.Model):
    # there is one enrolled student per class
    student = models.ForeignKey(EnrolledStudent)
    course = models.ForeignKey(Course)
    assessments = models.ManyToManyField(Assessment)
    submitted = models.BooleanField(default=False)
    week = models.IntegerField()
    grade_percent = models.IntegerField()
    engagement_percent = models.IntegerField()
    note = models.CharField(max_length=500)

    def __unicode__(self):
        full_name = self.student.first_name + ' ' + self.student.last_name
        return unicode(full_name + ' (Week ' + str(self.week) + ')')