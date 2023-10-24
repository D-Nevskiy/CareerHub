from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants.users import (NAME_LENGTH, EMAIL_LENGTH,
                                  TELEGRAM_LENGTH, PHONE_NUMBER_LENGTH,
                                  COMPANY_NAME_LENGTH, ROLE_LENGTH)


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'

    ROLES = (
        (USER, USER),
        (ADMIN, ADMIN)
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True
    )
    first_name = models.CharField(max_length=NAME_LENGTH)
    last_name = models.CharField(max_length=NAME_LENGTH)
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True
    )
    telegram = models.URLField(
        max_length=TELEGRAM_LENGTH,
        null=False,
        blank=True
    )
    phone_number = models.CharField(
        max_length=PHONE_NUMBER_LENGTH,
        blank=True
    )
    company = models.CharField(
        max_length=COMPANY_NAME_LENGTH,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=ROLE_LENGTH,
        choices=ROLES,
        default=USER,
        blank=True
    )
    is_active = models.BooleanField(default=False)
    username = None

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
