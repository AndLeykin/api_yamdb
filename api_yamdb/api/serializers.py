from rest_framework import serializers
from django.db.models import Avg

import datetime as dt

from reviews.models import Comment, Review, Category, Genre, Title, GenreTitle
from reviews.validators import MIN_YEAR


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year or value < MIN_YEAR:
            raise serializers.ValidationError('Проверьте год произведения!')
        return value

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError('Необходимо указать жанр.')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        genre_title_query = GenreTitle.objects.filter(title=instance.id)
        representation['genre'] = []
        for genre_title_instance in genre_title_query:
            genre_representation = [genre_title_instance.genre.name,
                                    genre_title_instance.genre.slug]
            representation['genre'].append(genre_representation)
        representation['category'] = [instance.category.name,
                                      instance.category.slug]
        return representation


class TitleReadSerializer(serializers.ModelSerializer):
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
    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
