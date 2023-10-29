from django.db import models

from core.constants.vacancies import (VACANCY_NAME_LENGTH, VACANCY_TEXT_LENGTH)
from shared_info.models import Schedule, Skill, EducationLevel, Specialization, \
    Location
from users.models import User


class Vacancy(models.Model):
    """
    Модель, представляющая вакансию.

    Атрибуты:
        - name (str): Название вакансии.
        - author (User): Автор вакансии.
        - location: Город вакансии.
        - text (str): Описание вакансии.
        - pub_date (datetime): Дата публикации вакансии.
        - schedule (ManyToManyField): График работы.
        - specialization (ManyToManyField): Направление специальности.
        - required_skills (ManyToManyField): Ключевые навыки.
        - required_education_level (ManyToManyField): Грейд.

    Мета:
        - verbose_name: Вакансия.
        - verbose_name_plural: Вакансии.

    Методы:
        - __str__(): Возвращает название вакансии в виде строки.
    """
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
    location = models.ForeignKey(
        Location,
        related_name='vacancies',
        on_delete=models.CASCADE,
        verbose_name='Локация',
        help_text='Выберите локацию'
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
    salary = models.CharField(
        verbose_name='Зарплата',
        max_length=VACANCY_NAME_LENGTH,
        null=False,
        help_text='Введите зарплату или зарплатную вилку'
    )
    schedule = models.ManyToManyField(
        Schedule,
        related_name='vacancies',
        through='vacancies.VacancySchedule',
        verbose_name='График работы',
        help_text='Выберите желаемый график работы'
    )
    specialization = models.ManyToManyField(
        Specialization,
        related_name='vacancies',
        through='vacancies.VacancySpecialization',
        verbose_name='Направление специальности',
        help_text='Выберите желаемое направление специальности'
    )
    required_skills = models.ManyToManyField(
        Skill,
        related_name='vacancies',
        through='vacancies.VacancySkills',
        verbose_name='Ключевые навыки',
        help_text='Выберите желаемые ключевые навыки'
    )
    required_education_level = models.ManyToManyField(
        EducationLevel,
        related_name='vacancies',
        through='vacancies.VacancyEducationLevel',
        verbose_name='Грейд',
        help_text='Выберите грейд'
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.name


class VacancySkills(models.Model):
    """
    Модель, представляющая связь между вакансией и ключевыми навыками.

    Атрибуты:
        - vacancy (Vacancy): Вакансия.
        - skill (Skill): Ключевой навык.

    Мета:
        - verbose_name: Скилы в вакансии.
        - verbose_name_plural: Скилы в вакансиях.

    Методы:
        - __str__(): Возвращает строку вида "Вакансия – Ключевой навык".
    """
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
    """
    Модель, представляющая связь между вакансией и грейдами.

    Атрибуты:
        - vacancy (Vacancy): Вакансия.
        - education_level (EducationLevel): Грейд вакансии.

    Мета:
        - verbose_name: Грейд в вакансии.
        - verbose_name_plural: Грейды в вакансиях.

    Методы:
        - __str__(): Возвращает строку вида "Вакансия – Грейд вакансии".
    """
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


class VacancySchedule(models.Model):
    """
    Модель, представляющая связь между вакансией и графиком работы.

    Атрибуты:
        - vacancy (Vacancy): Вакансия.
        - schedule (Schedule): График работы вакансии.

    Мета:
        - verbose_name: График работы в вакансии.
        - verbose_name_plural: Графики работы в вакансиях.

    Методы:
        - __str__(): Возвращает строку вида "Вакансия – График
        работы вакансии".
    """
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        verbose_name='Вакансия',
        related_name='vacancy_schedule'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        verbose_name='График работы в вакансии',
        related_name='vacancy_schedule'
    )

    class Meta:
        verbose_name = 'График работы в вакансии'
        verbose_name_plural = 'Графики работы в вакансиях'

    def __str__(self):
        return f'{self.vacancy} – {self.schedule}'


class VacancySpecialization(models.Model):
    """
   Модель, представляющая связь между вакансией и направлением специальности.

   Атрибуты:
       - vacancy (Vacancy): Вакансия.
       - specialization (Specialization): Направление специальности.

   Мета:
       - verbose_name: Направление специальности.
       - verbose_name_plural: Направления специальностей.

   Методы:
       - __str__(): Возвращает строку вида "Вакансия – Направление
       специальности".
   """
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        verbose_name='Вакансия',
        related_name='vacancy_specialization'
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        verbose_name='Направление специальности',
        related_name='vacancy_specialization'
    )

    class Meta:
        verbose_name = 'Направление специальности'
        verbose_name_plural = 'Направления специальностей'

    def __str__(self):
        return f'{self.vacancy} – {self.specialization}'
