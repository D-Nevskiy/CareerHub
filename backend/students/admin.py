from django.contrib import admin

from students.models import (Student, StudentSkills,
                             StudentEducationLevel, StudentSpecialization,
                             StudentSchedule)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели Student.

    Параметры:
        - list_display: Поля, которые будут отображаться в списке студентов.
        - list_filter: Поля, по которым можно фильтровать список студентов.
        - search_fields: Поля, по которым можно выполнять поиск студентов.

    Модель:
        - Student.
    """
    list_display = ('last_name', 'first_name')
    list_filter = ('schedule', 'specialization')
    search_fields = ('last_name', 'first_name')


@admin.register(StudentSkills)
class StudentSkillsAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели StudentSkills.

    Параметры:
        - list_display: Поля, которые будут отображаться в списке связей
        студентов и ключевых навыков.
        - list_filter: Поля, по которым можно фильтровать список связей.
        - search_fields: Поля, по которым можно выполнять поиск связей.

    Модель:
        - StudentSkills.
    """
    list_display = ('student', 'skill')
    list_filter = ('student', 'skill')
    search_fields = (
    'student__first_name', 'student__last_name', 'skill__name')


@admin.register(StudentEducationLevel)
class StudentEducationLevelAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели StudentEducationLevel.

    Параметры:
        - list_display: Поля, которые будут отображаться в списке связей
        студентов и грейдов.
        - list_filter: Поля, по которым можно фильтровать список связей.
        - search_fields: Поля, по которым можно выполнять поиск связей.

    Модель:
        - StudentEducationLevel.
    """
    list_display = ('student', 'education_level')
    list_filter = ('student', 'education_level')
    search_fields = (
    'student__first_name', 'student__last_name', 'education_level__name')


@admin.register(StudentSpecialization)
class StudentSpecializationAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели StudentSpecialization.

    Параметры:
        - list_display: Поля, которые будут отображаться в списке связей
        студентов и направлений специальности.
        - list_filter: Поля, по которым можно фильтровать список связей.
        - search_fields: Поля, по которым можно выполнять поиск связей.

    Модель:
        - StudentSpecialization.
    """
    list_display = ('student', 'specialization')
    list_filter = ('student', 'specialization')
    search_fields = (
    'student__first_name', 'student__last_name', 'specialization__name')


@admin.register(StudentSchedule)
class StudentScheduleAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели StudentSchedule.

    Параметры:
        - list_display: Поля, которые будут отображаться в списке связей
        студентов и графиков работы.
        - list_filter: Поля, по которым можно фильтровать список связей.
        - search_fields: Поля, по которым можно выполнять поиск связей.

    Модель:
        - StudentSchedule.
    """
    list_display = ('student', 'schedule')
    list_filter = ('student', 'schedule')
    search_fields = (
    'student__first_name', 'student__last_name', 'schedule__name')
