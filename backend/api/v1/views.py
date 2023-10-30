from typing import Any, Tuple, Dict

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_200_OK)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, ViewSet

from api.v1.permissions import (IsAuthorOrAdmin, IsVacancyAuthorOrAdmin,
                                IsAdminUser)
from api.v1.serializers import (StudentSerializer, StudentDetailSerializer,
                                VacancySerializer, VacancyReadSerializer,
                                MatchingStudentSerializer,
                                VacancySmallReadSerializer)
from core.pagination import CustomPagination
from students.models import Student, FavoriteStudent, CompareStudent
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

    def get_permissions(self) -> Any:
        """
        Возвращает соответствующий permission в зависимости от действия.
        """
        if self.action == 'list':
            return (IsAdminUser(),)
        return (IsAuthenticatedOrReadOnly(),)

    def get_serializer_class(self) -> Any:
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
        - perform_create(self, serializer, **kwargs): Сохраняет
        автора вакансии.
        - update(self, request, *args, **kwargs): Обновляет вакансию.
    """
    permission_classes = (IsAuthorOrAdmin,)
    pagination_class = CustomPagination

    def get_queryset(self) -> Any:
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

    def get_serializer_class(self) -> Any:
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == 'retrieve':
            return VacancyReadSerializer
        if self.action == 'list':
            return VacancySmallReadSerializer
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
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        required_skills = vacancy.required_skills.all()

        matching_students = Student.objects.filter(
            skills__in=required_skills)

        filters = {}
        for param in ['location', 'education_level', 'schedule']:
            value = request.query_params.get(param)
            if value:
                filters[param] = value

        if filters:
            matching_students = matching_students.filter(**filters)

        matching_students = sorted(
            matching_students,
            key=lambda student: len(
                set(required_skills) & set(student.skills.all())),
            reverse=True
        )

        serializer = MatchingStudentSerializer(
            matching_students,
            many=True,
            context={'vacancy_id': vacancy_id}
        )
        return Response(serializer.data)


class FavoriteStudentViewSet(ViewSet):
    """
    ViewSet для управления избранными студентами.

    Методы:
        - get(request): Предоставляет список избранных студентов.
        - post(request, student_id): Добавляет студента в избранное.
        - delete(request, student_id): Удаляет студента из избранного.

    Permissions:
        - Доступно только авторизованным пользователям.

    Attributes:
        - request: Запрос пользователя.
        - student_id: ID студента, который добавляется в или удаляется
        из избранного.

    Returns:
        - HTTP_201_CREATED: Если студент успешно добавлен в избранное.
        - HTTP_400_BAD_REQUEST: Если студент уже находится в
        избранном (при добавлении).
        - HTTP_204_NO_CONTENT: Если студент успешно удален из избранного.
        - HTTP_404_NOT_FOUND: Если студент не найден в
        избранном (при удалении).
    """
    @staticmethod
    def get_favorites(request) -> Response:
        """Предоставляет список избранных студентов."""
        favorites = FavoriteStudent.objects.filter(user=request.user)

        student_ids = [favorite.student_id for favorite in favorites]
        students = Student.objects.filter(pk__in=student_ids)
        serializer = StudentSerializer(students, many=True,
                                       context={'request': request})

        return Response(serializer.data, status=HTTP_200_OK)

    @staticmethod
    def post(request, student_id: int) -> Response:
        """Добавляет студента в избранное."""
        student = get_object_or_404(Student, pk=student_id)
        favorite, created = FavoriteStudent.objects.get_or_create(
            user=request.user,
            student=student
        )
        if created:
            return Response({"detail": "Студент добавлен в избранное"},
                            status=HTTP_201_CREATED)
        return Response({"detail": "Студент уже в избранном"},
                        status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, student_id: int) -> Response:
        """Удаляет студента из избранного."""
        student = get_object_or_404(Student, pk=student_id)
        favorite = FavoriteStudent.objects.filter(user=request.user,
                                                  student=student)
        if favorite:
            favorite.delete()
            return Response({"detail": "Студент удален из избранного"},
                            status=HTTP_204_NO_CONTENT)
        return Response({"detail": "Студент не найден в избранном"},
                        status=HTTP_404_NOT_FOUND)


class CompareStudentViewSet(ViewSet):
    """
    ViewSet для управления списком сравнения студентов.

    Методы:
        - get_compare(request): Возвращает список студентов в списке сравнения.
        - post(request, student_id): Добавляет студента в список сравнения.
        - delete(request, student_id): Удаляет студента из списка сравнения.

    Permissions:
        - Доступно только авторизованным пользователям.

    Attributes:
        - request: Запрос пользователя.
        - student_id: ID студента, который добавляется в или удаляется
        из списка сравнения.

    Returns:
        - HTTP_200_OK: Возвращает список студентов в списке
        сравнения (при get_compare).
        - HTTP_201_CREATED: Если студент успешно добавлен в список сравнения.
        - HTTP_400_BAD_REQUEST: Если студент уже находится в списке
        сравнения (при добавлении).
        - HTTP_204_NO_CONTENT: Если студент успешно удален из списка сравнения.
        - HTTP_404_NOT_FOUND: Если студент не найден в списке
        сравнения (при удалении).
    """
    @staticmethod
    def get_compare(request) -> Response:
        """Возвращает список студентов в списке сравнения."""
        compare_students = CompareStudent.objects.filter(user=request.user)
        student_ids = [compare.student_id for compare in compare_students]
        students = Student.objects.filter(pk__in=student_ids)
        serializer = StudentDetailSerializer(students,
                                             many=True,
                                             context={'request': request})

        return Response(serializer.data, status=HTTP_200_OK)

    @staticmethod
    def post(request, student_id: int) -> Response:
        """Добавляет студента в список сравнения."""
        student = get_object_or_404(Student, pk=student_id)
        compare, created = CompareStudent.objects.get_or_create(
            user=request.user,
            student=student
        )
        if created:
            return Response(
                {"detail": "Студент добавлен в список для сравнения"},
                status=HTTP_201_CREATED
            )
        return Response({"detail": "Студент уже в списке для сравнения"},
                        status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, student_id: int) -> Response:
        """Удаляет студента из списка сравнения."""
        student = get_object_or_404(Student, pk=student_id)
        favorite = FavoriteStudent.objects.filter(user=request.user,
                                                  student=student)
        if favorite:
            favorite.delete()
            return Response(
                {"detail": "Студент удалён из списка для сравнения"},
                status=HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "Студент не найден в списке для сравнения"},
            status=HTTP_404_NOT_FOUND
        )
