from rest_framework import permissions


class CustomCinemaPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            return obj.seller.id == request.user.id
        return True


class OnlySellerCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_seller
        return True
