from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from datetime import timezone

class User(AbstractUser):
    username = None
    identity_no = models.TextField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.TextField()
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'identity_no'
    REQUIRED_FIELDS = []
    

    def __str__(self):
        return self.name

