from rest_framework.permissions import AllowAny, SAFE_METHODS, BasePermission


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False
    
    def has_object_permission(self, request, view, obj):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_object_permission(request, view, obj)
        return False


class AuthorAllStaffAllButEditOrReadOnly(BasePermission):

    edit_methods = ("PUT", "PATCH")

    """def has_permission(self, request, view):
        print('Checks has ')
        if request.user.is_authenticated:
            return True"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True
        
        print('Checks ', obj.author , ' ', request.user)

        if obj.author == request.user:
            return True
        print('Checks2')

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
    

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
