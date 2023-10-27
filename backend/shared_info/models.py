from django.db import models
from core.constants.shared_info import (SKILL_NAME_LENGTH,
                                        EDUCATIONLEVEL_NAME_LENGTH,
                                        SPECIALIZATION_NAME_LENGTH,
                                        SCHEDULE_NAME_LENGTH,
                                        COURSE_NAME_LENGTH)


class Skill(models.Model):
    """
    Модель для хранения информации о ключевых навыках.

    Attributes:
        - name (str): Название ключевого навыка.

    Methods:
        - __str__(): Возвращает строковое представление навыка (название).

    Meta:
        - verbose_name (str): Отображаемое название
        модели (единственное число).
        - verbose_name_plural (str): Отображаемое название
        модели (множественное число).
    """
    name = models.CharField(max_length=SKILL_NAME_LENGTH)

    class Meta:
        verbose_name = 'Скилл'
        verbose_name_plural = 'Скиллы'

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    """
    Модель для хранения информации о грейдах образования.

    Attributes:
        - name (str): Название грейда образования.

    Methods:
        - __str__(): Возвращает строковое представление грейда (название).

    Meta:
        - verbose_name (str): Отображаемое название
        модели (единственное число).
        - verbose_name_plural (str): Отображаемое название
        модели (множественное число).
    """
    name = models.CharField(max_length=EDUCATIONLEVEL_NAME_LENGTH)

    class Meta:
        verbose_name = 'Грейд'
        verbose_name_plural = 'Грейды'

    def __str__(self):
        return self.name


class Specialization(models.Model):
    """
    Модель для хранения информации о специализациях.

    Attributes:
        - name (str): Название специализации.

    Methods:
        - __str__(): Возвращает строковое представление
        специализации (название).

    Meta:
        - verbose_name (str): Отображаемое название
        модели (единственное число).
        - verbose_name_plural (str): Отображаемое название
        модели (множественное число).
    """
    name = models.CharField(max_length=SPECIALIZATION_NAME_LENGTH)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    """
    Модель для хранения информации о графиках работы.

    Attributes:
        - name (str): Название графика работы.

    Methods:
        - __str__(): Возвращает строковое представление
        графика работы (название).

    Meta:
        - verbose_name (str): Отображаемое название
        модели (единственное число).
        - verbose_name_plural (str): Отображаемое название
        модели (множественное число).
    """
    name = models.CharField(max_length=SCHEDULE_NAME_LENGTH)

    class Meta:
        verbose_name = 'График'
        verbose_name_plural = 'Графики'

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Модель для хранения информации о курсах.

    Attributes:
        - name (str): Название курса.

    Methods:
        - __str__(): Возвращает строковое представление курса (название).

    Meta:
        - verbose_name (str): Отображаемое название
        модели (единственное число).
        - verbose_name_plural (str): Отображаемое название
        модели (множественное число).
    """
    name = models.CharField(max_length=COURSE_NAME_LENGTH)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курс'

    def __str__(self):
        return self.name
