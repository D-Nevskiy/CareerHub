from django.contrib.auth.models import AbstractUser
from django.db import models

EDUCATION_LEVEL_CHOICES = [
    ('Intern', 'Intern'),
    ('Junior', 'Junior'),
    ('Middle', 'Middle'),
    ('Senior', 'Senior'),
]

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


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    email = models.EmailField(unique=True, max_length=254)
    telegram = models.URLField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=10, choices=EDUCATION_LEVEL_CHOICES)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_LEVEL_CHOICES)
    portfolio = models.URLField()
    experience = models.TextField()
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.user_profile.username + 'Student Profile'


class Recruiter(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)

    def __str__(self):
        return self.user_profile.username + 'Recruiter Profile'
