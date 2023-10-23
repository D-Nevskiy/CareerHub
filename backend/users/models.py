from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    telegram = models.URLField(max_length=100, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, unique=True, null=True)
    company = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username + 'Recruiter Profile'
