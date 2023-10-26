from django.contrib import admin
from .models import Skill, EducationLevel, Specialization, Schedule, Course


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
