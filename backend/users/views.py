import requests
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @action(
        methods=['get'], detail=False,
        url_path='activation_user', permission_classes=(AllowAny,)
    )
    def activate(self, request, uid, token, format=None):
        print(request)
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/api/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())