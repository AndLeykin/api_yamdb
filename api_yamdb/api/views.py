from django.db import IntegrityError
from django.http import Http404
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Comment, Review, Category, Genre, Title
from .mixins import ListAddDeleteViewset
from .permissions import (
    IsAdminOrReadOnlyPermission, ReviewAndComments
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
)
from .filters import GenreFilter


class CategoryViewSet(ListAddDeleteViewset):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListAddDeleteViewset):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = GenreFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewAndComments,)

    def get_title(self) -> Title:
        title_qs = Title.objects.filter(pk=self.kwargs.get("title_id"))
        if not title_qs.exists():
            raise Http404
        else:
            return title_qs.first()

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())

    def perform_create(self, serializer):
        title = self.get_title()
        try:
            serializer.save(
                title=title,
                author=self.request.user,
            )
        except IntegrityError:
            raise ValidationError({
                'title': 'Вы уже добавили отзыв на это произведение'
            })


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewAndComments,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self) -> Review:
        review_qs = Review.objects.filter(
            pk=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id")
        )
        if not review_qs.exists():
            raise Http404
        else:
            return review_qs.first()

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.get_review())

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            review_id=review,
            author=self.request.user,
        )
