from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

BIG_LENGTH = 256
SMALL_LENGH = 50


class Category(models.Model):
    """Модель категорий.
    У одного произведения может быть одна категррия.
    """
    name = models.CharField(max_length=BIG_LENGTH)
    slug = models.SlugField(max_length=SMALL_LENGH, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=BIG_LENGTH)
    slug = models.SlugField(max_length=SMALL_LENGH, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений, к которым пишут комменты."""
    name = models.CharField(max_length=BIG_LENGTH)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи произведений и жанров.
    Подробнее об это в уроке 9 спринта 8.
    """
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        # Принудительное ограничение в бд
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='unique_genre_and_title'
            )
        ]

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        db_column='title_id',
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
