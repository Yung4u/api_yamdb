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
