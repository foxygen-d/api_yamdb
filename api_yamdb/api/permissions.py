from rest_framework import permissions


class ProfileOwner(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class RolePermissions(permissions.DjangoModelPermissions):

    perms_map = {
        'GET': ['view_%(model_name)s'],
        'POST': ['add_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        role_perms = request.user._role.permissions
        return request.user.is_superuser or all([
            role_perms.filter(codename=perm).exists() for perm in perms])


class RolePermissionsOrReadOnly(RolePermissions):

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                or request.method in permissions.SAFE_METHODS)


class RolePermissionsAuthorOrReadOnly(RolePermissionsOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or super().has_permission(request, view))

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)
