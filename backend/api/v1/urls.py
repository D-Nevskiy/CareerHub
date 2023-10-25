from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet, EmailViewSet

router = DefaultRouter()

router.register(r'users', CustomUserViewSet)

urlpatterns = [
    # Нужно зацепить 11 строку вместо 13. Пока хз как))
    # path('', include(router.urls)),
    path('activate/<str:uid>/<str:token>/', EmailViewSet.as_view({"get": "activate"}), name="activate"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
