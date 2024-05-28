from django.db import models
from login.models import *
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.BooleanField(default=False)
    birthdate = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=12)
    email = models.EmailField(unique=True, null=True, blank=True)
