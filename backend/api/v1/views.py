from typing import Any, Tuple, Dict
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, ViewSet

from api.v1.permissions import (IsAuthorOrAdmin, IsVacancyAuthorOrAdmin,
                                IsAdminUser)
from api.v1.serializers import (StudentSerializer, StudentDetailSerializer,
                                VacancySerializer, VacancyReadSerializer,
                                MatchingStudentSerializer)
from core.pagination import CustomPagination
from students.models import Student
from vacancies.models import Vacancy


class StudentViewSet(ReadOnlyModelViewSet):
    """
    Этот ViewSet предоставляет список и детальную информацию о студентах.

    Доступен только просмотр.

    Attributes:
        - queryset: Запрос, возвращающий все объекты Student.
        - pagination_class: Кастомный класс пагинации.
    """
    queryset = Student.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        """
        Возвращает соответствующий permission в зависимости от действия.
        """
        if self.action == 'list':
            return (IsAdminUser(),)
        return (IsAuthenticatedOrReadOnly(),)

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == 'list':
            return StudentSerializer
        elif self.action == 'retrieve':
            return StudentDetailSerializer


class VacancyViewSet(ModelViewSet):
    """
    Этот ViewSet предоставляет CRUD-функциональность для вакансий.

    Создание вакансии доступно всем авторизованным пользователям.
    Просмотр, редактирование и удаление вакансий доступно только их авторам.

    Attributes:
        - serializer_class: Сериализатор, используемый для преобразования
        данных ваканций.
        - pagination_class: Кастомный класс пагинации.

    Permissions:
        - permission_classes: Список классов разрешений для ViewSet.
        Установлены стандартные разрешения Django REST framework.

    Methods:
        - perform_create(self, serializer, **kwargs): Сохраняет автора вакансии.
        - update(self, request, *args, **kwargs): Обновляет вакансию.
    """
    permission_classes = (IsAuthorOrAdmin,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает queryset вакансий в зависимости от пользователя.

        Если пользователь - администратор, возвращаются все вакансии.
        В противном случае возвращаются только вакансии,
        принадлежащие пользователю.

        Returns:
            QuerySet: QuerySet вакансий в соответствии с правами
            доступа пользователя.
        """
        user = self.request.user

        if user.is_admin:
            return Vacancy.objects.all()

        return Vacancy.objects.filter(author=user)

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == 'retrieve':
            return VacancyReadSerializer
        return VacancySerializer

    def perform_create(self, serializer, **kwargs: Any) -> None:
        """
        Сохранение автора вакансии.

        Args:
            serializer: Сериализатор вакансии.
            **kwargs: Дополнительные аргументы.

        Returns:
            None
        """
        serializer.save(author=self.request.user)

    def update(self, request, *args: Tuple[Any],
               **kwargs: Dict[Any, Any]) -> Response:
        """
        Обновление вакансии.

        Args:
            request: Запрос.
            *args: Позиционные аргументы.
            **kwargs: Ключевые аргументы.

        Returns:
            Response: Ответ с данными вакансии после обновления.
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MatchingStudentsViewSet(ViewSet):
    """
    Этот ViewSet предоставляет список студентов, подходящих
    для конкретной вакансии.

    Список доступен только для автора вакансии и администраторов.

    Attributes:
        - permission_classes: Список классов разрешений для ViewSet.
        - pagination_class: Кастомный класс пагинации.

    Methods:
        - list(request, vacancy_id): Возвращает список студентов, подходящих
        для указанной вакансии.

    Args:
        request: Запрос.
        vacancy_id: ID вакансии.

    Returns:
        Response: Список студентов, подходящих для вакансии.
    """
    permission_classes = (IsVacancyAuthorOrAdmin,)
    pagination_class = CustomPagination

    @staticmethod
    def list(request: Any, vacancy_id: int) -> Response:
        try:
            vacancy = get_object_or_404(Vacancy, id=vacancy_id)
            required_skills = vacancy.required_skills.all()

            matching_students = Student.objects.filter(
                skills__in=required_skills
            ).distinct()
            matching_students = sorted(
                matching_students,
                key=lambda student: len(set(required_skills)
                                        & set(student.skills.all())),
                reverse=True
            )

            serializer = MatchingStudentSerializer(
                matching_students,
                many=True,
                context={'vacancy_id': vacancy_id}
            )
            return Response(serializer.data)
        except Vacancy.DoesNotExist:
            return Response({"detail": "Вакансия не найдена"},
                            status=HTTP_404_NOT_FOUND)
