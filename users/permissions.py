from rest_framework.permissions import BasePermission


class IsUserProfileOwner(BasePermission):
    """
    check if authenticated user is owner of the profile
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsUserAddressOwner(BasePermission):
    """
    check if authenticated user is owner of the address
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
