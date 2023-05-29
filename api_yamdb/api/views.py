from rest_framework import permissions, status, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comment, Review, Category, Genre, Title
from .mixins import ListAddDeleteViewset
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
from rest_framework.response import Response

class CategoryViewSet(ListAddDeleteViewset):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListAddDeleteViewset):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnlyPermission,)
    # Здесь надо выяснитить, какую пагинацию делаем
    pagination_class = LimitOffsetPagination
    # Не пойму, здесь нужен вообще фильтр или нет. Вроде нигде не просят
    filter_backends = (filters.SearchFilter,)
    search_fields = ('genre',)


    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get("title_id"))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            title = Title.objects.get(pk=self.kwargs.get("title_id"))
        except Title.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid(raise_exception=False):
            try:
                serializer.save(
                    title=title,
                    author=self.request.user,
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED,
                )
            except Exception:
                pass

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            review_id=Review.objects.get(pk=self.kwargs.get("review_id")),
            author=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            title = Title.objects.get(pk=self.kwargs.get("title_id"))
        except Title.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            review = Review.objects.get(pk=self.kwargs.get("review_id"), title_id=title.pk)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid(raise_exception=False):
            try:
                serializer.save(
                    review_id=review,
                    author=self.request.user,
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED,
                )
            except Exception:
                pass

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action in ['update', 'destroy', 'partial_update']:
            return (IsAuthorOrModeratorOrAdmin(),)
        elif self.action in ['create']:
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()
