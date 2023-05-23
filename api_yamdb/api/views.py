from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comment, Review
from .permissions import IsAuthor, IsAuthorOrModeratorOrAdmin
# Create your views here.
from .serializers import (CommentSerializer,
                          ReviewSerializer)


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
