from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own store profile"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to edit their own store profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        print(obj.id)
        print(request.user)
        return obj.id == request.user.id


class UpdateOwnItem(permissions.BasePermission):
    """Allows users to update their own items"""

    def has_object_permission(self, request, view, obj):
        """"""
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.store_user:
            return obj.store_user.id == request.user.id

        return False
