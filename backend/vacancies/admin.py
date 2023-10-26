from django.contrib import admin
from .models import (Vacancy, VacancySkills,
                     VacancyEducationLevel, VacancySpecialization)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date')
    list_filter = ('author', 'pub_date', 'schedule', 'specialization')
    search_fields = ('name', 'author__username')


@admin.register(VacancySkills)
class VacancySkillsAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'skill')
    list_filter = ('vacancy', 'skill')
    search_fields = ('vacancy__name', 'skill__name')


@admin.register(VacancyEducationLevel)
class VacancyEducationLevelAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'education_level')
    list_filter = ('vacancy', 'education_level')
    search_fields = ('vacancy__name', 'education_level__name')


@admin.register(VacancySpecialization)
class VacancySpecializationAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'specialization')
    list_filter = ('vacancy', 'specialization')
    search_fields = ('vacancy__name', 'specialization__name')
