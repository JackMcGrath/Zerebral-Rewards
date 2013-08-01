from django.db import models
from schools.models import School

# teacher
class Teacher(models.Model):
    # do not require school in case it's not in the db
    school = models.ForeignKey(School, blank=True, null=True)

    def __unicode__(self):
        return unicode('Teacher of ' + self.school.school_name)