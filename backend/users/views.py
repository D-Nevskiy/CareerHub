from typing import Tuple, Any

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from api.v1.permissions import IsAdminUser
from core.celery.celery_app import send_activation_email, activate_user
from core.pagination import CustomPagination
from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    Кастомный ViewSet для работы с пользователями.

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
    pagination_class = CustomPagination

    def get_permissions(self) -> Tuple:
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == 'list':
            return (IsAdminUser(),)
        return (AllowAny(),)

    def perform_create(self, serializer) -> Any:
        """
        Создает пользователя и отправляет ему письмо со ссылкой
        на активацию аккаунта.

        :param serializer: Сериализатор, используемый для
        создания пользователя.
        :return: Созданный пользователь.
        """
        user = serializer.save()
        # Используем стандартный генератор токенов.
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = reverse_lazy('activate',
                                       kwargs={'uid': uid, 'token': token})
        recipient_list = [user.email]
        # Отправляем письмо с помощью celery.
        send_activation_email.delay(activation_link, recipient_list)

        return user

    @action(
        methods=['get'], detail=False,
        url_path='activation_user', permission_classes=(AllowAny,)
    )
    @swagger_auto_schema(
        operation_description="Активация пользователя",
        responses={204: "Успешная активация пользователя",
                   400: "Ошибка активации"},
    )
    def activate(self, request, uid, token, format=None) -> Response:
        """
        Активирует пользователя с заданным UID и токеном.

        :param request: Объект запроса.
        :param uid: Уникальный идентификатор пользователя.
        :param token: Токен активации.
        :param format: Формат ответа (по умолчанию None).
        :return: Ответ, указывающий на успешную активацию или ошибку.
        """
        try:
            # Отправляем запрос на активацию аккаунта с помощью celery.
            activate_user.delay(uid, token)
        except Exception as error:
            return Response(error, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_204_NO_CONTENT)
