from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants.users import (NAME_LENGTH, EMAIL_LENGTH,
                                  TELEGRAM_LENGTH, PHONE_NUMBER_LENGTH,
                                  COMPANY_NAME_LENGTH, ROLE_LENGTH)
from core.validators import validate_phone_number


class UserManager(BaseUserManager):
    """
    Менеджер пользователей.

    Этот менеджер обеспечивает создание и управление пользователями в системе.

    Methods:
        - _create_user(email, password, **extra_fields): Создает и сохраняет
        пользователя с заданным email и паролем.
        - create_user(email, password=None, **extra_fields): Создает и
        сохраняет обычного пользователя.
        - create_superuser(email, password, **extra_fields): Создает и
        сохраняет суперпользователя.

    Attributes:
        - use_in_migrations: Флаг, указывающий, что этот менеджер
        используется в миграциях.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с заданным email и паролем.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param extra_fields: Дополнительные поля пользователя.
        :return: Созданный пользователь.
        """
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param extra_fields: Дополнительные поля пользователя.
        :return: Созданный пользователь.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя.

        :param email: Email суперпользователя.
        :param password: Пароль суперпользователя.
        :param extra_fields: Дополнительные поля суперпользователя.
        :return: Созданный суперпользователь.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя.

    Эта модель представляет пользователя системы и содержит информацию о нём.

    Attributes:
        - USER: Константа, представляющая роль обычного пользователя.
        - ADMIN: Константа, представляющая роль администратора.
        - ROLES: Кортеж с доступными ролями пользователя.

        - USERNAME_FIELD: Поле, используемое в качестве имени
        пользователя (email).
        - REQUIRED_FIELDS: Поля, которые необходимо заполнить при
        создании пользователя.

    Fields:
        - avatar: Поле для загрузки аватара пользователя (не обязательно).
        - first_name: Поле для имени пользователя (обязательно).
        - last_name: Поле для фамилии пользователя (обязательно).
        - email: Поле для email-адреса пользователя (уникальное, обязательно).
        - telegram: Поле для ссылки на профиль пользователя в
        Telegram (не обязательно).
        - phone_number: Поле для номера телефона пользователя (не обязательно).
        - company: Поле для названия компании пользователя (не обязательно).
        - role: Поле для определения роли пользователя (пользователь или
        администратор. При создании автоматически выбирается "пользователь").
        - is_active: Флаг, указывающий активен ли пользователь
        (изначально False. Меняется на True после подтверждения
        почты через письмо).
        - username: Поле имени пользователя (не используется).

    Meta:
        - verbose_name: Отображаемое имя модели в единственном числе.
        - verbose_name_plural: Отображаемое имя модели во множественном числе.

    Methods:
        - __str__(): Возвращает строковое представление пользователя
        в формате "Имя Фамилия".
    """
    USER = 'user'
    ADMIN = 'admin'

    ROLES = (
        (USER, USER),
        (ADMIN, ADMIN)
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    object = UserManager()

    avatar = models.ImageField(
        'Изображение профиля',
        upload_to='avatars/',
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=NAME_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=NAME_LENGTH
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_LENGTH,
        unique=True
    )
    telegram = models.URLField(
        'Ссылка на Telegram',
        max_length=TELEGRAM_LENGTH,
        null=False,
        blank=True
    )
    phone_number = models.CharField(
        max_length=PHONE_NUMBER_LENGTH,
        blank=True,
        validators=[validate_phone_number],
        verbose_name='Номер телефона',
        help_text='Введите номер телефона'
    )
    company = models.CharField(
        'Компания',
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
        """
        Возвращает строковое представление пользователя.

        :return: Строковое представление в формате "Имя Фамилия".
        """
        return f'{self.first_name} {self.last_name}'
