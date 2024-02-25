from django.shortcuts import get_object_or_404
from functools import wraps
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import CartItem, WishlistItem


class IsCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.cart.profile.user:
            return True
        return False


def is_cart_owner(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        cartitem_id = kwargs.get("cartitem_id")
        cart_item = get_object_or_404(CartItem, id=cartitem_id)
        permission = IsCartOwner()
        if not permission.has_object_permission(request, None, cart_item):
            return Response(
                {"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view


class IsWishlistOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.wishlist.profile.user:
            return True
        return False


def is_wishlist_owner(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        wishlistitem_id = kwargs.get("wishlistitem_id")
        wishlist_item = get_object_or_404(WishlistItem, id=wishlistitem_id)
        permission = IsWishlistOwner()
        if not permission.has_object_permission(request, None, wishlist_item):
            return Response(
                {"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view
