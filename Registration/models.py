from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class ExtUser(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length = 20, blank=False)
    mobile = models.IntegerField(blank=False)
    dob = models.DateField(blank = False)


