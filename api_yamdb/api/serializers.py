from rest_framework import serializers
from django.db.models import Avg

import datetime as dt

from reviews.models import Comment, Review, Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = '__all__'
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений.
    Для пост запросов.
    """
    # Тут какой то головняк. В пачке увидел совет наставниика, что надо делать
    # два сериализатора - для чтения и записи.
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title

    # Это чтобы неьлзя было добавить произведение будущего года
    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений.
    Пока решил сделать два сер. для  одного вьюсета. Спр. 8 ур.12.
    PS Сериализаторы для связанных моделей
    """
    # Махинации с вложенными сериализаторами делаются, чтобы апи
    # выдавала строку из связанной модели, а не цифру слага
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    # PS сериализаторы доп возможности
    def get_rating(self, obj):
        rating = (
            obj.reviews.filter(title=obj)
            .aggregate(Avg('score'))
            ['score__avg']
        )
        if rating:
            return int(rating)
        else:
            return None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')
        read_only_fields = ('title_id',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review_id',)
