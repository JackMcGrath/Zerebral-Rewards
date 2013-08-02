from django.db import models
from students.models import EnrolledStudent

# actions for an action plan
class Action(models.Model):
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode('Action Plan Action')

class ActionPlan(models.Model):
    # an enrolledstudent gives us student & class
    student = models.ForeignKey(EnrolledStudent)
    actions = models.ManyToManyField(Action)
    goal = models.CharField(max_length=100, null=True, blank=True)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    needs_revising = models.BooleanField(default=False)
    revising_notes = models.CharField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    ACTION_PLAN_TYPES = (
        ('weekly', 'Weekly'),
    )
    type = models.CharField(max_length=50, choices=ACTION_PLAN_TYPES)