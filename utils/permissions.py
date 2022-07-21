from cinemas.models import Cinema
from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class OwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user == object.cinema.owner


class OnlySelfManagerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Cinema):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and obj.owner == request.user


class OnlySelfManagerPermissionFinancial(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.cinema.owner == request.user


class IsTicketOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user
