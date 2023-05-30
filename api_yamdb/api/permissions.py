from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj.author == request.user or request.user.role == 'moderator' or (
                request.user.is_admin))
