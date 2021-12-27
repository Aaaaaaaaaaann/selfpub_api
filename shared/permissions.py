from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Prevent users from updating and deleting content
    of other users.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE') and obj.author.id != request.user.id:
            return False
        return True


class IsUserAccount(permissions.BasePermission):
    """Prevent users from "updating and deleting personal data
    of other users.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE') and obj.id != request.user.id:
            return False
        return True