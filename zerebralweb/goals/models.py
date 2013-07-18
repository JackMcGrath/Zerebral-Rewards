from django.db import models
from parents.models import Parent
from students.models import Student


# goal oriented models
class ActionPlan(models.Model):
	student = models.ForeignKey(Student)
	goal_one = models.CharField(max_length=500)
	goal_two = models.CharField(max_length=500)
	goal_three = models.CharField(max_length=500)
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
    parent = models.ForeignKey(Parent)