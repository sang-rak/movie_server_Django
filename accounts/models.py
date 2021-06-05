from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import FloatField

class User(AbstractUser):
    imageBase64 = models.ImageField(blank=True)
    male = models.FloatField(null=True)
    age = models.FloatField(null=True)

