from rest_framework import permissions


class ReviewCommentPermission(permissions.BasePermission):
    """Проверка на доступ к операциям с Review и Comment"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moder
                or obj.author == request.user)


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка на доступ к операциям с User"""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.method == 'PATCH' and request.user.is_user:
            return (request.data.get('username') == request.user.username)
        return (
            request.user.is_superuser
            or request.user.is_admin
            or request.user.is_staff
        )


class IsAdminorReadOnly(permissions.BasePermission):
    """Проверка на доступ к операциям с Category, Genre и Title"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
