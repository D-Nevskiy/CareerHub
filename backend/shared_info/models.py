from django.db import models
from core.constants.shared_info import (SKILL_NAME_LENGTH,
                                        EDUCATIONLEVEL_NAME_LENGTH,
                                        SPECIALIZATION_NAME_LENGTH,
                                        SCHEDULE_NAME_LENGTH,
                                        COURSE_NAME_LENGTH)


class Skill(models.Model):
    name = models.CharField(max_length=SKILL_NAME_LENGTH)

    class Meta:
        verbose_name = 'Скилл'
        verbose_name_plural = 'Скиллы'

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    name = models.CharField(max_length=EDUCATIONLEVEL_NAME_LENGTH)

    class Meta:
        verbose_name = 'Грейд'
        verbose_name_plural = 'Грейды'

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=SPECIALIZATION_NAME_LENGTH)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    name = models.CharField(max_length=SCHEDULE_NAME_LENGTH)

    class Meta:
        verbose_name = 'График'
        verbose_name_plural = 'Графики'

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=COURSE_NAME_LENGTH)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курс'

    def __str__(self):
        return self.name
