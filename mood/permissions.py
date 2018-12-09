from rest_framework.permissions import BasePermission

class MoodObjectPermissions(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user