from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


# class OnlySelfManagerPermission(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method == "PATCH":
#             return request.user.is == request.user.id
#         return True
