from django.db import models
from students.models import Student
from teachers.models import Teacher
from django.contrib.auth.models import User

# ZerebralUser is how we link together Django's User model and School, Teacher, Parent, and/or Student profiles
class ZerebralUser(models.Model):
    # these are used to control access to views and determine user type
    class Meta:
        permissions = (("is_teacher", "Has access to teacher dashboard"),
                       ("is_student", "Has access to student dashboard"),)

    # link up with Django's user model
    user = models.OneToOneField(User)

    # has this user accepted the TOS?
    tos_accepted = models.BooleanField(default=False)

    # link to the actual profile depending on the user type (mutiple are allowed)
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    student = models.ForeignKey(Student, blank=True, null=True)