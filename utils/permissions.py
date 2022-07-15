from rest_framework import permissions
from cinemas.models import Cinema


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class OnlySelfManagerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Cinema):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj: ParkingLot):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return obj.owner == request.user
