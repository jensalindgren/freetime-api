from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD, or OPTIONS requests.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        """
        Write permissions are only allowed to the owner of the snippet.
        """
        return obj.owner == request.user


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD, or OPTIONS requests.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        """
        Write permissions are only allowed to the owner of the snippet.
        """
        return obj.owner == request.user or request.user.is_staff


class IsStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Custom permission to check if the user is staff or not
    """
    def has_permission(self, request, view):
        """
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD, or OPTIONS requests.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        """
        Write permissions are only allowed to the owner of the snippet.
        """
        return request.user and request.user.is_staff