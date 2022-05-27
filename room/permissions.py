from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            print("test ", klass)
            if view.action in actions:
                return klass().has_permission(request, view)
        return False
    
    def has_object_permission(self, request, view, obj):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_object_permission(request, view, obj)
        return False


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
