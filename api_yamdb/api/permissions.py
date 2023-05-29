from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Добавлять произведения, категории и жанры может только администратор."""
    message = 'Добавлять может только администратор'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                )


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.role in ['admin', 'moderator']
                )
