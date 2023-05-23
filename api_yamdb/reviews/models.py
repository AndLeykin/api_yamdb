from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "admin"
        MODERATOR = "moderator", "moderator"
        USER = "user", "user"

    role = models.TextField(choices=Role.choices, default=Role.USER)
    bio = models.TextField(null=True)


class Title(models.Model):
    ...


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10), ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="author_and_title_unique",
                fields=["author", "title_id"],
            ),
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
