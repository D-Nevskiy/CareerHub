from rest_framework import permissions

from vacancies.models import Vacancy


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Пользовательское разрешение для доступа только автору и администратору.

    Атрибуты:
        - message: Сообщение об ошибке, если разрешение не пройдено.

    message:
        - Сообщение об ошибке.

    Методы:
        - has_object_permission(self, request, view, obj): Определяет, имеет ли
        пользователь доступ к объекту.
    """
    message = "Только автор и администратор могут редактировать этот объект."

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Определяет, имеет ли пользователь доступ к объекту.

        Args:
            request: Запрос пользователя.
            view: Представление, которое обрабатывает запрос.
            obj: Объект, к которому идёт обращение.

        Returns:
            bool: True, если пользователь имеет доступ,
            False в противном случае.
        """

        return obj.author == request.user or request.user.is_admin


class IsVacancyAuthorOrAdmin(permissions.BasePermission):
    """
    Пользовательское разрешение для доступа к подбору студентов только
    автору вакансии.

    message:
        - Сообщение об ошибке.

    Методы:
        - has_permission(self, request, view): Проверяет, имеет ли пользователь
        доступ к данному представлению.
    """

    message = ("Вы не автор этой вакансии или её не существует. "
               "Доступ запрещен.")

    def has_permission(self, request, view):
        # Проверяем является ли пользователь автором вакансии.
        vacancy_id = view.kwargs.get('vacancy_id')
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return False

        if request.user.is_anonymous:
            return False
        return vacancy.author == request.user or request.user.is_admin
