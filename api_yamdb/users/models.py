from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    ('user', 'пользователь'),
    ('admin', 'администратор'),
    ('moderator', 'модератор'),
)
ROLE_MAX_LENGTH = 10
SECRET_KEY_MAX_LENGTH = 256
USERNAME_MAX_LENGTH = 150


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Тип пользователя',
        max_length=ROLE_MAX_LENGTH,
        choices=USER_ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=SECRET_KEY_MAX_LENGTH,
        blank=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=SECRET_KEY_MAX_LENGTH,
        blank=True,
    )

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором"""
        return (
            self.role == 'admin'
            or self.is_superuser
        )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='me_username_constraint',
            ),
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email',
            ),
        ]
        ordering = ('-username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
