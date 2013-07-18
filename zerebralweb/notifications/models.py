from django.db import models
from django.contrib.auth.models import User

# notifications for users
class Notification(models.Model):
	initiator = models.ForeignKey(User, related_name='notification_initiator')
	recipient = models.ForeignKey(User, related_name='notification_recipient')

	NOTIFICATION_TYPES = (
	    ('metgoal', 'Met Goal'),
	)
	type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)

	body = models.CharField(max_length=100)

	read = models.BooleanField(default=False)