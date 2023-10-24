import requests
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class ActivateUser(APIView):
    def get(self, request, uid, token, format=None):
        print(request)
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/api/auth/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())
