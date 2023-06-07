from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
ADMIN = 'admin'
MODER = 'moderator'
USER_ROLES = (
    (USER, 'пользователь'),
    (ADMIN, 'администратор'),
    (MODER, 'модератор'),
)
ROLE_MAX_LENGTH = 20
SECRET_KEY_MAX_LENGTH = 256
USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Тип пользователя',
        max_length=ROLE_MAX_LENGTH,
        choices=USER_ROLES,
        default=USER
    )
    password = models.CharField(
        'Пароль',
        max_length=SECRET_KEY_MAX_LENGTH,
        blank=True,
    )
    email = models.EmailField(
        'Почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором"""
        return (
            self.role == ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором"""
        return self.role == MODER

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='me_username_constraint',
            ),
        ]
        ordering = ('-username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
