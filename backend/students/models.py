from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.constants.students import (NAME_LENGTH, EMAIL_LENGTH,
                                     TELEGRAM_LENGTH, PHONE_NUMBER_LENGTH,
                                     ROLE_LENGTH, PORTFOLIO_LENGTH,
                                     EXPERIENCE_LENGTH, STUDENT_MAX_AGE,
                                     STUDENT_MIN_AGE)
from core.validators import validate_phone_number
from shared_info.models import (Skill, EducationLevel, Specialization,
                                Schedule, Course)


class Student(models.Model):
    """
    Модель для хранения информации о студентах.

    Attributes:
        - avatar: Фото студента.
        - first_name: Имя студента.
        - last_name: Фамилия студента.
        - email: Электронная почта студента.
        - sex: Пол студента.
        - age: Возраст студента.
        - telegram: Ссылка на Telegram студента.
        - phone_number: Номер телефона студента.
        - portfolio: Портфолио студента.
        - experience: Опыт работы студента.
        - specialization: Направление специальности студента.
        - course: Название курса, на котором учится студент.
        - education_level: Грейд студента.
        - skills: Ключевые навыки студента.
        - schedule: График работы студента.

    Methods:
        - __str__(): Возвращает строковое представление студента в
        формате "Фамилия Имя".
    """

    SEX_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина')
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name='Фото студента',
        help_text='Выберите фото'
    )
    first_name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Имя студента',
        help_text='Введите имя студента'
    )
    last_name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Фамилия студента',
        help_text='Введите фамилию студента'
    )
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта студента',
        help_text='Введите электронную почту студента'
    )
    sex = models.CharField(
        max_length=ROLE_LENGTH,
        choices=SEX_CHOICES,
        null=False,
        blank=True,
        verbose_name='Пол студента',
        help_text='Выберите пол студента'
    )
    age = models.PositiveSmallIntegerField(
        null=False,
        blank=True,
        validators=[
            MinValueValidator(STUDENT_MIN_AGE, 'Возраст не может быть ниже 18!'),
            MaxValueValidator(STUDENT_MAX_AGE, 'Слишком большой возраст!')
        ],
        verbose_name='Возраст студента',
        help_text='Введите возраст студента'
    )
    telegram = models.URLField(
        max_length=TELEGRAM_LENGTH,
        null=False,
        blank=True,
        verbose_name='Ссылка на Telegram студента',
        help_text='Введите ссылку на Telegram студента'
    )
    phone_number = models.CharField(
        max_length=PHONE_NUMBER_LENGTH,
        blank=True,
        validators=[validate_phone_number],
        verbose_name='Номер телефона студента',
        help_text='Введите номер телефона студента'
    )
    portfolio = models.URLField(
        max_length=PORTFOLIO_LENGTH,
        blank=True,
        verbose_name='Портфолио студента',
        help_text='Введите ссылку на портфолио студента'
    )
    experience = models.TextField(
        max_length=EXPERIENCE_LENGTH,
        blank=True,
        verbose_name='Опыт работы студента',
        help_text='Укажите опыт работы студента'
    )
    specialization = models.ManyToManyField(
        Specialization,
        related_name='students',
        through='students.StudentSpecialization',
        verbose_name='Направление специальности',
        help_text='Выберите направление специальности'
    )
    course = models.ForeignKey(
        Course,
        related_name='course',
        on_delete=models.CASCADE,
        verbose_name='Название курса',
        help_text='Выберите название курса'
    )
    education_level = models.ManyToManyField(
        EducationLevel,
        related_name='students',
        through='students.StudentEducationLevel',
        verbose_name='Грейд студента',
        help_text='Выберите грейд'
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='students',
        through='students.StudentSkills',
        verbose_name='Ключевые навыки',
        help_text='Выберите ключевые навыки'
    )
    schedule = models.ManyToManyField(
        Schedule,
        related_name='students',
        through='students.StudentSchedule',
        verbose_name='График работы',
        help_text='Выберите график работы'
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class StudentSkills(models.Model):
    """
   Модель для хранения связей между студентами и навыками.

   Attributes:
       - student: Связь с моделью студента.
       - skill: Связь с моделью навыка.

   Methods:
       - __str__(): Возвращает строковое представление связи в
       формате "Студент – Навык".
   """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='student_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Скилл студента',
        related_name='student_skills'
    )

    class Meta:
        verbose_name = 'Скиллы студента'
        verbose_name_plural = 'Скиллы студентов'

    def __str__(self):
        return f'{self.student} – {self.skill}'


class StudentEducationLevel(models.Model):
    """
    Модель для хранения связей между студентами и их грейдом.

    Attributes:
        - student: Связь с моделью студента.
        - education_level: Связь с моделью уровня образования.

    Methods:
        - __str__(): Возвращает строковое представление связи в формате "Студент – Грейд".

    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='student_education_level'
    )
    education_level = models.ForeignKey(
        EducationLevel,
        on_delete=models.CASCADE,
        verbose_name='Грейд студента',
        related_name='student_education_level'
    )

    class Meta:
        verbose_name = 'Грейд студента'
        verbose_name_plural = 'Грейды студентов'

    def __str__(self):
        return f'{self.student} – {self.education_level}'


class StudentSchedule(models.Model):
    """
    Модель для хранения связей между студентами и графиком работы.

    Attributes:
        - student: Связь с моделью студента.
        - schedule: Связь с моделью графика работы.

    Methods:
        - __str__(): Возвращает строковое представление связи в
        формате "Студент – График работы".

    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='student_schedule'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        verbose_name='График работы студента',
        related_name='student_schedule'
    )

    class Meta:
        verbose_name = 'График работы студента'
        verbose_name_plural = 'Графики работы студентов'

    def __str__(self):
        return f'{self.student} – {self.schedule}'


class StudentSpecialization(models.Model):
    """
    Модель для хранения связей между студентами и специализациями.

    Attributes:
        - student: Связь с моделью студента.
        - specialization: Связь с моделью специализации.

    Methods:
        - __str__(): Возвращает строковое представление связи в
        формате "Студент – Специализация".
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='student_specialization'
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        verbose_name='Специализация студента',
        related_name='student_specialization'
    )

    class Meta:
        verbose_name = 'Специализация студента'
        verbose_name_plural = 'Специализации студентов'

    def __str__(self):
        return f'{self.student} – {self.specialization}'
