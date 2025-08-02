from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)
