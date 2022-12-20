from rest_framework.permissions import BasePermission

class IsActive(BasePermission):
    """ 
        Allow access only to "is active" users
        
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_active