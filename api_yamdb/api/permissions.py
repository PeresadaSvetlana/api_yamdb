from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_anonymous
                and request.method not in permissions.SAFE_METHODS):
            return False
        else:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role in ('admin')
            )


class IsAdminOrSuperOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user.is_admin)


class IsAdminModeratorAuthororReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')
