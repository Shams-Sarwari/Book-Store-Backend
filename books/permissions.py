from django.shortcuts import get_object_or_404
from functools import wraps
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Review, Reply


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        return False


class AuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        return False


class AdminOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "PATCH" and request.user == obj.profile.user:
            return True
        if request.method == "DELETE" and (
            request.user == obj.profile.user or request.user.is_superuser
        ):
            return True
        return False


def admin_owner_or_readonly_review(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        review_id = kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        permission = AdminOrOwnerOrReadOnly()
        if not permission.has_object_permission(request, None, review):
            return Response(
                {"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view


def admin_owner_or_readonly_reply(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        reply_id = kwargs.get("reply_id")
        reply = get_object_or_404(Reply, id=reply_id)
        permission = AdminOrOwnerOrReadOnly()
        if not permission.has_object_permission(request, None, reply):
            return Response(
                {"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view
