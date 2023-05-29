from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re

from .models import User, SECRET_KEY_MAX_LENGTH, USERNAME_MAX_LENGTH


EMAIL_MAX_LENGTH = 254

USERNAME_ERROR = 'Недопустимое имя пользователя.'
EMAIL_USED_ERROR = 'Эта почта уже используется.'
EMAIL_INCORRECT_ERROR = 'Неверная почта.'


def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


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
            raise serializers.ValidationError(USERNAME_ERROR)
        return value


class MeUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        required=True, max_length=USERNAME_MAX_LENGTH
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if username.casefold() == 'me' or (
                not re.match(r'^[\w.@+-]+\Z', username)):
            raise serializers.ValidationError(
                detail={'username': USERNAME_ERROR})
        user = get_user(username)
        if user and user.email != email:
            raise serializers.ValidationError(
                detail={'email': EMAIL_INCORRECT_ERROR})
        if User.objects.filter(email=email).exists() and not user:
            raise serializers.ValidationError(
                detail={'email': EMAIL_USED_ERROR})
        return data
