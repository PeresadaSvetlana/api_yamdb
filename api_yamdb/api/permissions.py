from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
 
        return bool(request.user and request.user.is_staff)


class IsAdminOrSuperOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )
        )

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )
        )