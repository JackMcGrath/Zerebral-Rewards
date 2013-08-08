from django.db import models


# parent
class Parent(models.Model):
    # parent's name
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    # parent's email
    email = models.EmailField(max_length=254)