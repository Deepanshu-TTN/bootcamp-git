'''Custom API Permission classes'''
from rest_framework import permissions


## PERMISSION CLASSES
class IsStaffUser(permissions.BasePermission):
    '''Permission class to check if the user is staff or not'''
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
    

class IsOwnerOrStaffUser(permissions.BasePermission):
    '''Permission class to check if the object is owned by a user or if the user is staff'''
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff: return True
        
        if hasattr(obj, 'customer'):
            return obj.customer == request.user
        
        return False