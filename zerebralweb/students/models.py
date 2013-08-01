from django.db import models
from badges.models import Badge
from goals.models import Goal
from classes.models import Course


# this is how we track students without them joining yet and link them via join codes for the course
class EnrolledStudent(models.Model):
    course = models.ForeignKey(Course)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    join_code = models.CharField(max_length=50)
    # has a student been linked with this enrollment?
    linked = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.first_name + ' ' + self.last_name + ' enrolled in ' + self.course.name)


# student
class Student(models.Model):
    # has the parent permitted this student to use zerebral?
    consent_from_parent = models.BooleanField(default=False)

    # the digital signature for this student
    consent_signed_by = models.CharField(max_length=100, blank=True, null=True)

    # parent's email to request consent
    parent_email = models.EmailField(max_length=254)

    # linked courses
    enrolled_courses = models.ManyToManyField(EnrolledStudent, blank=True, null=True, related_name='enrolled_courses')
    archived_courses = models.ManyToManyField(EnrolledStudent, blank=True, null=True, related_name='archived_courses')

    # this should be updated every time an evaluation is submitted (essentially caching the total point calculation)
    pts_earned = models.IntegerField(default=0)
    pts_spent = models.IntegerField(default=0)

    goals_earned = models.ManyToManyField(Goal, blank=True, null=True)
    badges_earned = models.ManyToManyField(Badge, blank=True, null=True)

    def __unicode__(self):
        return unicode('Zerebral Student Profile')