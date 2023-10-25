from django.db import models

from core.constants.vacancies import (VACANCY_NAME_LENGTH, VACANCY_TEXT_LENGTH,
                                      VACANCY_SCHEDULE_LENGTH)
from shared_info.models import Schedule, Skill, EducationLevel
from users.models import User


class Vacancy(models.Model):
    name = models.CharField(
        verbose_name='Название вакансии',
        max_length=VACANCY_NAME_LENGTH,
        db_index=True,
        null=False,
        help_text='Введите название вакансии'
    )
    author = models.ForeignKey(
        User,
        related_name='vacancies',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        max_length=VACANCY_TEXT_LENGTH,
        null=False,
        verbose_name='Описание',
        help_text='Введите описание вакансии'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False
    )
    schedule = models.ManyToManyField(
        Schedule,
        related_name='vacancies',
        verbose_name='График работы',
        help_text='Выберите желаемый график работы'
    )
    required_skills = models.ManyToManyField(
        Skill,
        related_name='vacancies',
        through='vacancies.VacancySkills'
    )
    required_education_level = models.ManyToManyField(
        EducationLevel,
        related_name='vacancies',
        through='vacancies.VacancyEducationLevel'
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.name


class VacancySkills(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        verbose_name='Вакансия',
        related_name='vacancy_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Скил в вакансии',
        related_name='vacancy_skills'
    )

    class Meta:
        verbose_name = 'Скилы в вакансии'
        verbose_name_plural = 'Скилы в вакансиях'

    def __str__(self):
        return f'{self.vacancy} – {self.skill}'


class VacancyEducationLevel(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        verbose_name='Вакансия',
        related_name='vacancy_education_level'
    )
    education_level = models.ForeignKey(
        EducationLevel,
        on_delete=models.CASCADE,
        verbose_name='Грейд в вакансии',
        related_name='vacancy_education_level'
    )

    class Meta:
        verbose_name = 'Грейд в вакансии'
        verbose_name_plural = 'Грейд в вакансиях'

    def __str__(self):
        return f'{self.vacancy} – {self.education_level}'
