from django.db import models

SPECIALIZATION_LEVEL_CHOICES = [
    ('Software Development', 'Software Development'),
    ('Quality Assurance', 'Quality Assurance'),
    ('Analytics', 'Analytics'),
    ('Design', 'Desing'),
    ('Management', 'Management'),
    ('Marketing', 'Management'),
    ('Administation', 'Administation'),
    ('Human Resources', 'Human Resources'),
]


class EducationLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True)
    telegram = models.URLField(max_length=100, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, unique=True)
    company = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_LEVEL_CHOICES)
    portfolio = models.URLField(blank=True)
    experience = models.TextField(blank=True)
    education_level = models.ManyToManyField(EducationLevel)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.first_name + self.last_name
