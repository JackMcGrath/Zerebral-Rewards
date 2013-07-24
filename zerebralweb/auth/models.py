from django.db import models
from parents.models import Parent
from students.models import Student
from teachers.models import Teacher
from django.contrib.auth.models import User
from schools.models import School

# ZerebralUser is how we link together Django's User model and School, Teacher, Parent, and/or Student profiles
class ZerebralUser(models.Model):
    # these are used to control access to views and determine user type
    class Meta:
        permissions = (("is_school", "Has access to school dashboard"),
                       ("is_teacher", "Has access to teacher dashboard"),
                       ("is_parent", "Has access to parent dashboard"),
                       ("is_student", "Has access to student dashboard"),)
    
    # link up with Django's user model
    user = models.OneToOneField(User)

    # has this user accepted the TOS?
    tos_accepted = models.BooleanField(default=False)

    # zerebral unique ID
    zerebral_id = models.CharField(max_length=50, unique=True)

    # link to the actual profile depending on the user type (mutiple are allowed)
    school = models.ForeignKey(School, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    parent = models.ForeignKey(Parent, blank=True, null=True)
    student = models.ForeignKey(Student, blank=True, null=True)



# used to invite parents, teachers, and students (initiator can be school, parent, or teacher)
class Invite(models.Model):
    INVITE_TYPES = (
        ('teacher', 'Invite Teacher'),
        ('student', 'Invite Student'),
        ('parent', 'Invite Parent'),
    )
    type = models.CharField(max_length=50, choices=INVITE_TYPES)

    # invitation code
    code = models.CharField(max_length=50)

    # who created this invite?
    initiator = models.ForeignKey(User)