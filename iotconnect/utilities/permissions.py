from rest_framework import permissions


class PermissionsNotSet(permissions.BasePermission):
    """
    Default permission
    """

    def has_object_permission(self, request, view, obj):
        pass
        # raise NotImplementedError("Permissions should be set explicitly: %s" % type(view).__name__)

    def has_permission(self, request, view):
        pass
        # raise NotImplementedError("Permissions should be set explicitly: %s" % type(view).__name__)
