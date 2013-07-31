from django.db import models




class GoalCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)


class Goal(models.Model):
    name = models.CharField(max_length=100)
    usd_cost = models.DecimalField(max_digits=15, decimal_places=2)
    point_cost = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(GoalCategory)
    active = models.BooleanField(default=False)