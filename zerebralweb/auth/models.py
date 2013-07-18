from django.db import models
from parents.models import Parent
from students.models import Student
from teachers.models import Teacher
from django.contrib.auth.models import User
from schools.models import School

# ZerebralUser is how we link together Django's User model and School, Teacher, Parent, and/or Student profiles
class ZerebralUser(models.Model):
	# link up with Django's user model
    user = models.OneToOneField(User)

    # has this user accepted the TOS?
    tos_accepted = models.BooleanField(default=False)

    # zerebral unique ID
    zerebral_id = models.CharField(max_length=50, unique=True)

    # link to the actual profile depending on the user type
    school = models.ForeignKey(School)
    teacher = models.ForeignKey(Teacher)
    parent = models.ForeignKey(Parent)
    student = models.ForeignKey(Student)



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