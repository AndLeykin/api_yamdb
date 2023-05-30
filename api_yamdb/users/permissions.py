from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )

    def has_object_permission(self, request, view, instance):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )
