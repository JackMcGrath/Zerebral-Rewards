from django.db import models

# school
class School(models.Model):
    school_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

# each term can have any number of point categories with a specific weight
class PointCategory(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(default=1.0, max_digits=15, decimal_places=2)