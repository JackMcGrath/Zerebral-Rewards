from django.db import models
from auth.models import ZerebralUser

# notifications for users
class Notification(models.Model):
    initiator = models.ForeignKey(ZerebralUser, related_name='notification_initiator', blank=True, null=True)
    recipient = models.ForeignKey(ZerebralUser, related_name='notification_recipient')

    NOTIFICATION_TYPES = (
        ('newgoal', 'New Goal Available'),
        ('earnedgoal', 'Earned Goal'),
        ('deniedgoal', 'Denied Goal'),
        ('earnedbadge', 'Earned Badge'),
        ('apneedrevise', 'Action Plan Needs Revising'),
        ('apapproved', 'Action Plan Approved'),
        ('earnedpoints', 'Earned Points'),
        ('message', 'Message'),
    )
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)

    body = models.CharField(max_length=500)

    read = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode('Message to ' + self.recipient.user.username)