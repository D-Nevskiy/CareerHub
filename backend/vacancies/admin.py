from django.contrib import admin
from vacancies.models import (Vacancy, VacancySkill, VacancyEducationLevel,
                              VacancySpecialization, VacancySchedule)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'pub_date')
    list_filter = ('author', 'pub_date', 'schedule', 'specialization')
    search_fields = ('name', 'author__username')


@admin.register(VacancySkill)
class VacancySkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'vacancy', 'skill')
    list_filter = ('vacancy', 'skill')
    search_fields = ('vacancy__name', 'skill__name')


@admin.register(VacancyEducationLevel)
class VacancyEducationLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'vacancy', 'education_level')
    list_filter = ('vacancy', 'education_level')
    search_fields = ('vacancy__name', 'education_level__name')


@admin.register(VacancySpecialization)
class VacancySpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'vacancy', 'specialization')
    list_filter = ('vacancy', 'specialization')
    search_fields = ('vacancy__name', 'specialization__name')


@admin.register(VacancySchedule)
class VacancyScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vacancy', 'schedule')
    list_filter = ('vacancy', 'schedule')
    search_fields = ('vacancy__name', 'schedule__name')
