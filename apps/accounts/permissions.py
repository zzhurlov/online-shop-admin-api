from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user
            and not request.user.is_anonymous
            and request.user.role == "SUPERUSER"
        ):
            return True
        return False
