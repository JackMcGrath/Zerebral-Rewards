from django.db import models
from schools.models import School
from badges.models import Badge

# student
class Student(models.Model):
    # has the parent permitted this student to use zerebral?
    consent_from_parent = models.BooleanField(default=False)
    # the digital signature for this student
    consent_signed_by = models.CharField(max_length=100, blank=True, null=True)
    school = models.ForeignKey(School)
    pts_spent = models.IntegerField(default=0)
    # this should be updated every time an evaluation is submitted (essentially caching the total point calculation)
    pts_earned = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge)