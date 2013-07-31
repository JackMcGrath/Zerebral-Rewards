from django.db import models
from badges.models import Badge



class Goal(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    point_cost = models.DecimalField(max_digits=15, decimal_places=2)

    # can this goal be earned?
    active = models.BooleanField(default=False)

    # the badge associated with earning this goal
    badge = models.ForeignKey(Badge)