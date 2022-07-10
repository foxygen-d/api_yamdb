from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (request.user.is_staff or request.user.role == 'admin' or
                    request.user.role == 'moderator' or
                    obj.author == request.user or
                    request.method == 'POST' and request.user.is_authenticated):
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True


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

        if not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only
        ):
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
