from django.db import models

# badges
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    icon = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)