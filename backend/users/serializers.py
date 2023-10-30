from djoser.serializers import UserSerializer
from users.models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор работы с пользователями."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'telegram',
            'phone_number',
            'company',
            'password',
            'is_active'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'telegram': {'required': False},
            'phone_number': {'required': False},
            'company': {'required': False},
            'is_active': {'required': False, 'read_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        if 'telegram' in validated_data:
            user.telegram = validated_data['telegram']
        if 'phone_number' in validated_data:
            user.phone_number = validated_data['phone_number']
        if 'company' in validated_data:
            user.company = validated_data['company']

        user.set_password(validated_data['password'])
        user.save()
        return user
