from rest_framework import permissions


class PostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        if request.method == "GET" and request.user.is_superuser:
            return True
        return False
