from django.db import models
from badges.models import Badge
from goals.models import Goal
from classes.models import Course
from students.helpers import generate_shortcode




# student
class Student(models.Model):
    # has the parent permitted this student to use zerebral?
    consent_from_parent = models.BooleanField(default=False)

    # the digital signature for this student
    consent_signed_by = models.CharField(max_length=200, blank=True, null=True)

    # parent's name
    parent_first_name = models.CharField(max_length=100, blank=True, null=True)
    parent_last_name = models.CharField(max_length=100, blank=True, null=True)

    # parent's email to request consent
    parent_email = models.EmailField(max_length=254)
    # the consent token sent in an email to confirm parent
    parent_token = models.CharField(max_length=50, blank=True, null=True, unique=True)

    # this should be updated every time an evaluation is submitted (essentially caching the total point calculation)
    pts_earned = models.IntegerField(default=0)
    pts_spent = models.IntegerField(default=0)

    goals_earned = models.ManyToManyField(Goal, blank=True, null=True)
    badges_earned = models.ManyToManyField(Badge, blank=True, null=True)

    def __unicode__(self):
        return unicode('Zerebral Student Profile')



# this is how we track students without them joining yet and link them via join codes for the course
class EnrolledStudent(models.Model):
    course = models.ForeignKey(Course)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, null=True)
    join_code = models.CharField(max_length=50, unique=True)
    # has a student been linked with this enrollment?
    student = models.ForeignKey(Student, blank=True, null=True)

    def save(self, *args, **kwargs):
        save_success = False
        while not save_success:
            try:
                # automatically generate a short code for each enrolled student before saving
                self.join_code = generate_shortcode(10)
                super(EnrolledStudent, self).save(*args, **kwargs)  # Call the "real" save() method.
                save_success = True
            except:
                # token collision, regen
                pass

    def __unicode__(self):
        return unicode(self.first_name + ' ' + self.last_name + ' enrolled in ' + self.course.name)