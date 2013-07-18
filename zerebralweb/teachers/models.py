from django.db import models
from schools.models import School

# teacher
class Teacher(models.Model):
    school = models.ForeignKey(School)