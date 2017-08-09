from rest_framework.permissions import BasePermission

class King(BasePermission):
    message = "You must be admin, staff, or author of this post."

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff or (obj.author == request.user):
            return True
        else:
            return False