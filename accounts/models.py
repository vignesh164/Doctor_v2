from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserDetails(models.Model):
    age = models.IntegerField(null=True)
    qualification = models.CharField(max_length=20, null=True)
    phone_no = models.IntegerField()


class User(AbstractUser):
    user_details = models.OneToOneField(UserDetails, null=True, on_delete=models.SET_NULL)
    pass