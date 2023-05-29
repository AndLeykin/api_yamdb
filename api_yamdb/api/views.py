from rest_framework import permissions, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comment, Review, Category, Genre, Title
from .permissions import (
    IsAuthorOrModeratorOrAdmin,
    IsAdminOrReadOnlyPermission
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    # Здесь надо выяснитить, какую пагинацию делаем
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    # Здесь надо выяснитить, какую пагинацию делаем
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnlyPermission,)
    # Здесь надо выяснитить, какую пагинацию делаем
    pagination_class = LimitOffsetPagination
    # Не пойму, здесь нужен вообще фильтр или нет. Вроде нигде не просят

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs.get("title_id"))

    def perform_create(self, serializer):
        serializer.save(
            title_id=Review.objects.get(pk=self.kwargs.get("title_id")),
            author=self.request.user,
        )

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action in ['update', 'destroy', 'partial_update']:
            return (IsAuthorOrModeratorOrAdmin(),)
        elif self.action in ['create']:
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Comment.objects.filter(
            review_id=self.kwargs.get("review_id"),
            review_id__title_id=self.kwargs.get("title_id")
        )

    def perform_create(self, serializer):
        serializer.save(
            review_id=Comment.objects.get(pk=self.kwargs.get("review_id")),
            author=self.request.user,
        )

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action in ['update', 'destroy', 'partial_update']:
            return (IsAuthorOrModeratorOrAdmin(),)
        elif self.action in ['create']:
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()
