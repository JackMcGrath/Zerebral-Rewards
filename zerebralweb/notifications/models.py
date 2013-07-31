from django.db import models
from auth.models import ZerebralUser

# notifications for users
class Notification(models.Model):
	initiator = models.ForeignKey(ZerebralUser, related_name='notification_initiator', blank=True, null=True)
	recipient = models.ForeignKey(ZerebralUser, related_name='notification_recipient')

	NOTIFICATION_TYPES = (
	    ('metgoal', 'Met Goal'),
	)
	type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)

	body = models.CharField(max_length=100)

	read = models.BooleanField(default=False)