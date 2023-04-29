from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def get_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return (
                request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.is_staff
                     or request.user.is_admin)
            )


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser


class IsAdminModeratorOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return ((obj.author == request.user)
                or (request.user.role == 'admin')
                or (request.user.role == 'moderator'))
