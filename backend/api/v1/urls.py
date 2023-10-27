from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

router = DefaultRouter()

router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'activation_user/<str:uid>/<str:token>/',
        CustomUserViewSet.as_view({'get': 'activate'}), name='activate'
    ),
    path('auth/', include('djoser.urls.jwt')),
]
