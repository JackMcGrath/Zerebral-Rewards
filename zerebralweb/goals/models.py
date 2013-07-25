from django.db import models
from parents.models import Parent
from students.models import Student
import datetime


# an action plan consists of multiple Actions (text describing what will be accomplished)
class Action(models.Model):
    goal = models.CharField(max_length=500)

# action plan
class ActionPlan(models.Model):
    student = models.ForeignKey(Student)
    goals = models.ManyToManyField(Action)
    approved = models.BooleanField(default=False)

# like an action plan, but weekly
class WeeklyActionPlan(models.Model):
    date = models.DateField(default=datetime.date.today)
    student = models.ForeignKey(Student)
    goals = models.ManyToManyField(Action)
    approved = models.BooleanField(default=False)


class GoalCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)


class Goal(models.Model):
    name = models.CharField(max_length=100)
    usd_cost = models.DecimalField(max_digits=15, decimal_places=2)
    point_cost = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(GoalCategory)
    action_plan = models.ForeignKey(ActionPlan)
    student = models.ForeignKey(Student)
    active = models.BooleanField(default=False)
    achieved = models.BooleanField(default=False)
    parent = models.ForeignKey(Parent)