from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
 
        return bool(request.user and request.user.is_staff)

class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or (request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.role == 'admin')