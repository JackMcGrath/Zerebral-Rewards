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