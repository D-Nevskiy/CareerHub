from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели User.

    Параметры:
        - list_display: Поля, которые будут отображаться в
        списке пользователей.
        - search_fields: Поля, по которым можно выполнять поиск пользователей.

    Модель:
        - User.
    """
    list_display = ('email', 'last_name', 'first_name')
    search_fields = ('email', 'last_name', 'first_name')
