from django.db import models
from django_localflavor_us.us_states import STATE_CHOICES


# school
class School(models.Model):
    school_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=100)

# each term can have any number of point categories with a specific weight
class PointCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    # whether this category can be edited by the teacher or not
    editable = models.BooleanField(default=False)
    weight = models.DecimalField(default=1.0, max_digits=15, decimal_places=2)

# terms hold classes, the point categories, and begin/end date
class Term(models.Model):
    school = models.ForeignKey(School)
    begin_date = models.DateField()
    end_date = models.DateField()
    # all of the point categories and their weights for this term
    point_categories = models.ManyToManyField(PointCategory)