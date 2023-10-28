from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views import (StudentViewSet, VacancyViewSet,
                          MatchingStudentsViewSet)
from users.views import CustomUserViewSet

router = DefaultRouter()

router.register(r'users', CustomUserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'vacancies', VacancyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'activation_user/<str:uid>/<str:token>/',
        CustomUserViewSet.as_view({'get': 'activate'}), name='activate'
    ),
    path('auth/', include('djoser.urls.jwt')),
    path(
        'matching/<int:vacancy_id>/',
        MatchingStudentsViewSet.as_view({'get': 'list'}),
        name='matching-students-list'
    ),
]
