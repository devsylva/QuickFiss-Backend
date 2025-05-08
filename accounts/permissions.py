from rest_framework.permissions import BasePermission

class IsArtisan(BasePermission):
    """
    Custom permission to only allow artisans to access a view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_artisan

class IsClient(BasePermission):
    """
    Custom permission to only allow clients to access a view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_client