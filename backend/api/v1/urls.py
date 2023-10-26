from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

router = DefaultRouter()

router.register(r'users', CustomUserViewSet)
#router.register(r'activation_user/<str:uid>/<str:token>/', CustomUserViewSet)

urlpatterns = [
    # Нужно зацепить 11 строку вместо 13. Пока хз как))
    path('', include(router.urls)),
    #path('activation_user/<str:uid>/<str:token>/', ActivateUser.as_view()),
    path('activation_user/<str:uid>/<str:token>/', CustomUserViewSet.as_view({'get': 'activate'}), name='activate'),
    #path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
