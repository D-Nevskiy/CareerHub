from rest_framework.permissions import BasePermission

from vacancies.models import Vacancy


class IsAuthorOrAdmin(BasePermission):
    """
    Пользовательское разрешение для доступа только автору и администратору.

    Attributes:
        message (str): Сообщение об ошибке, выводимое при отказе в доступе.

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


class IsVacancyAuthorOrAdmin(BasePermission):
    """
    Пользовательское разрешение для доступа к подбору студентов только
    автору вакансии.

    Attributes:
        message (str): Сообщение об ошибке, выводимое при отказе в доступе.

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


class IsAdminUser(BasePermission):
    """
    Проверяет, имеет ли пользователь статус администратора
    для доступа к ресурсу.

    Attributes:
        message (str): Сообщение об ошибке, выводимое при отказе в доступе.

    Methods:
        has_permission(self, request, view): Проверяет, имеет ли пользователь
        статус администратора.

    Args:
        request (HttpRequest): Объект запроса пользователя.
        view (APIView): Представление, к которому применяется разрешение.

    Returns:
        bool: True, если пользователь имеет статус администратора, и False в
        противном случае.
    """
    message = ("Доступ к данной странице предоставляется "
               "только администраторам.")

    def has_permission(self, request, view):
        return request.user.is_admin
