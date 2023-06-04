from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_year

NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
MIN_SCORE = 1
MAX_SCORE = 10
FOR_STR = 25


class Category(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Уникальный адрес', max_length=SLUG_MAX_LENGTH, unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name[:FOR_STR]


class Genre(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Уникальный адрес', max_length=SLUG_MAX_LENGTH, unique=True
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name[:FOR_STR]


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(
        'Год создания',
        validators=[validate_year]
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name[:FOR_STR]


class GenreTitle(models.Model):
    """Модель для связи произведений и жанров."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
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
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    text = models.TextField('Текст', )
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE), ]
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
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return f'Отзыв #{self.pk} на книгу {self.title.name}'


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=' id отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='пользователь',
    )
    text = models.TextField('Текст', )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return (f'Комментарий №{self.pk} к отзыву №{self.review_id.pk}'
                'на книгу {self.title.name}')
