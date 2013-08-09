from django.db import models
from django_localflavor_us.us_states import STATE_CHOICES


# school
class School(models.Model):
    school_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.school_name)

# each term can have any number of point categories with a specific weight
class PointCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    # whether this category can be edited by the teacher or not
    editable = models.BooleanField(default=False)
    weight = models.DecimalField(default=1.0, max_digits=10, decimal_places=2)

    def __unicode__(self):
        return unicode(self.name)

# terms hold classes, the point categories, and begin/end date
class Term(models.Model):
    alias = models.CharField(max_length=100)
    school = models.ForeignKey(School)
    begin_date = models.DateField()
    end_date = models.DateField()
    # all of the point categories and their weights for this term
    point_categories = models.ManyToManyField(PointCategory)

    def __unicode__(self):
        return unicode('Started on ' + str(self.begin_date))