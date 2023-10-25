from django.db import models
from shared_info.models import Skill, EducationLevel, Specialization, Schedule
from core.constants.students import (NAME_LENGTH, EMAIL_LENGTH,
                                     TELEGRAM_LENGTH, PHONE_NUMBER_LENGTH,
                                     COMPANY_NAME_LENGTH, ROLE_LENGTH,
                                     PORTFOLIO_LENGTH, EXPERIENCE_LENGTH)


class Student(models.Model):
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
    portfolio = models.URLField(
        max_length=PORTFOLIO_LENGTH,
        blank=True
    )
    experience = models.TextField(
        max_length=EXPERIENCE_LENGTH,
        blank=True
    )
    specialization = models.ForeignKey(
        Specialization,
        related_name='students',
        on_delete=models.CASCADE
    )
    education_level = models.ManyToManyField(
        EducationLevel,
        related_name='students',
        through='students.StudentEducationLevel'
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='students',
        through='students.StudentSkills'
    )
    schedule = models.ManyToManyField(
        Schedule,
        related_name='students',
        verbose_name='График работы',
        help_text='Выберите желаемый график работы'
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.first_name + self.last_name


class StudentSkills(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='student_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Скилл у студента',
        related_name='student_skills'
    )

    class Meta:
        verbose_name = 'Скиллы у студента'
        verbose_name_plural = 'Скиллы у студентов'

    def __str__(self):
        return f'{self.student} – {self.skill}'


class StudentEducationLevel(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='student_education_level'
    )
    education_level = models.ForeignKey(
        EducationLevel,
        on_delete=models.CASCADE,
        verbose_name='Грейд у студента',
        related_name='student_education_level'
    )

    class Meta:
        verbose_name = 'Грейд у студента'
        verbose_name_plural = 'Грейды у студентов'

    def __str__(self):
        return f'{self.student} – {self.education_level}'
