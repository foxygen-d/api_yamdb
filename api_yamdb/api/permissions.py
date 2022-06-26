from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.id == obj.author.id)


class IsModeratorOrReadOnly(permissions.BasePermission):

    ...


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True
