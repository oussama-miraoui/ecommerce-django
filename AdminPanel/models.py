from django.db import models
from products.models import *



class Admin(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, blank=True)
    date =models.DateTimeField(auto_now=True)

