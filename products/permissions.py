from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSellerOrAdmin(BasePermission):
    """
    check if authenticated user is seller of the product or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method is SAFE_METHODS:
            return True

        return obj.seller == request.user or request.user.is_admin


class IsUserOrReadOnly(BasePermission):
    """
    check if authenticated user is seller of the product or only viewer
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
