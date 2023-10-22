from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True)
    telegram = models.URLField(max_length=100, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, unique=True)
    company = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username + 'Recruiter Profile'

    USERNAME_FIELD = 'email'
