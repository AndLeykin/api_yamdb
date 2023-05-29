from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, SECRET_KEY_MAX_LENGTH, USERNAME_MAX_LENGTH


EMAIL_MAX_LENGTH = 254

USERNAME_ME_ERROR = 'Это имя пользователя запрещено.'


class CustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField(
        required=True, max_length=SECRET_KEY_MAX_LENGTH
    )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        max_length=EMAIL_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, value):
        if value.casefold() == 'me':
            raise serializers.ValidationError(USERNAME_ME_ERROR)
        return value


class UserSelfSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio',
        )


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        required=True, max_length=USERNAME_MAX_LENGTH
    )

    def validate_username(self, value):
        if value.casefold() == 'me':
            raise serializers.ValidationError(USERNAME_ME_ERROR)
        return value
