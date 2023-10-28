from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, ViewSet

from api.v1.serializers import (StudentSerializer, StudentDetailSerializer,
                                VacancySerializer, VacancyReadSerializer)
from students.models import Student
from vacancies.models import Vacancy


class StudentViewSet(ReadOnlyModelViewSet):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentSerializer
        elif self.action == 'retrieve':
            return StudentDetailSerializer


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return VacancyReadSerializer
        return VacancySerializer

    def perform_create(self, serializer, **kwargs: Any) -> None:
        serializer.save(author=self.request.user)


class MatchingStudentsViewSet(ViewSet):
    @staticmethod
    def list(request, vacancy_id):
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
                reverse=True)

            serializer = StudentSerializer(matching_students, many=True)
            return Response(serializer.data)
        except Vacancy.DoesNotExist:
            return Response({"detail": "Vacancy not found"}, status=HTTP_404_NOT_FOUND)
