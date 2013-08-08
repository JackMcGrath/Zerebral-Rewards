from django.db import models
from teachers.models import Teacher
from goals.models import Goal
from schools.models import Term


# a new course is created for each term by the teacher
class Course(models.Model):
    name = models.CharField(max_length=100)
    stub = models.CharField(max_length=100)
    course_id = models.CharField(max_length=100)
    goals = models.ManyToManyField(Goal, blank=True, null=True)
    teacher = models.ForeignKey(Teacher)
    term = models.ForeignKey(Term)

    def __unicode__(self):
        return unicode(self.name)