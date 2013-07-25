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



# used to invite parents or teachers
class TeacherParentInvite(models.Model):
    # invitation code
    code = models.CharField(max_length=50)

    # info that will be pre-filled when clicking an invite link
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    # who created this invite?
    initiator = models.ForeignKey(User)

# used to invite students (parent info attached)
class StudentInvite(TeacherParentInvite):
    parent_first_name = models.CharField(max_length=100)
    parent_last_name = models.CharField(max_length=100)
    parent_email = models.EmailField(max_length=254)