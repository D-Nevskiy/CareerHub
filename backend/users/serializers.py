from djoser.serializers import UserSerializer
from users.models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор работы с пользователями."""

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'telegram', 'phone_number', 'company', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
