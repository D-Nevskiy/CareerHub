from django.contrib import admin
from django.urls import path, include
from users.views import ActivateUser

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('api/', include('api.v1.urls')),
    path('api/activation_user/<str:uid>/<str:token>/', ActivateUser.as_view()),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]
