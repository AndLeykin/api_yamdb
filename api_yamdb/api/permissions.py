from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj.author == request.user or request.user.is_moderator or
            request.user.is_admin
        )


class ReviewAndComments(permissions.BasePermission):
    def _select_permision(self, request) -> permissions.BasePermission:
        if request.method == 'POST':
            return permissions.IsAuthenticated()
        elif request.method in ['PATCH', 'DELETE']:
            return IsAuthorOrModeratorOrAdmin()
        else:
            return permissions.AllowAny()

    def has_object_permission(self, request, view, obj):
        return self._select_permision(request).has_object_permission(
            request, view, obj
        )

    def has_permission(self, request, view):
        return self._select_permision(request).has_permission(request, view)
