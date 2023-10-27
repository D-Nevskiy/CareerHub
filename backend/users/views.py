import requests
from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    Пользовательский ViewSet для работы с пользователями.

    Этот ViewSet предоставляет эндпоинты для управления пользователями,
    включая активацию.

    Attributes:
        - queryset: Запрос, возвращающий все объекты User.
        - serializer_class: Сериализатор, используемый для преобразования
        данных пользователя.

    Permissions:
        - permission_classes: Список классов разрешений для ViewSet. Здесь
        установлен AllowAny для открытого доступа.

    Methods:
        - activate(self, request, uid, token, format=None): Активирует
        пользователя с заданным UID и токеном.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @action(
        methods=['get'], detail=False,
        url_path='activation_user', permission_classes=(AllowAny,)
    )
    @swagger_auto_schema(
        operation_description="Активация пользователя",
        responses={204: "Успешная активация пользователя",
                   400: "Ошибка активации"},
    )
    def activate(self, request, uid, token, format=None):
        """
        Активирует пользователя с заданным UID и токеном.

        :param request: Объект запроса.
        :param uid: Уникальный идентификатор пользователя.
        :param token: Токен активации.
        :param format: Формат ответа (по умолчанию None).
        :return: Ответ, указывающий на успешную активацию или ошибку.
        """
        print(request)
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/api/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())