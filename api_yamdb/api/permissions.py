from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.id == obj.author.id)


class IsSuperuser(permissions.IsAuthenticated):

    def has_permission(self, request):
        return request.user.is_superuser


class RolePermissions(permissions.DjangoModelPermissions):

    perms_map = {
        'GET': ['view_%(model_name)s'],
        'POST': ['add_%(model_name)s'],
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
        role_perms = request.user.role.permissions
        print(request.user)
        print(request.user.role)
        print(role_perms)
        print(perms)
        return request.user.is_superuser or all([
            role_perms.filter(codename=perm).exists() for perm in perms])
