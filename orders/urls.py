from django.urls import path
from .views import *

urlpatterns = [
    path("cart-items", cart_items, name="cart-items"),
    path("cart-items/<int:bookline_id>", cart_items, name="cart-items"),
    path("cart-item/<int:cartitem_id>", cart_item, name="cart-item"),
    path("wishlist", wishlist_items, name="wishlist-items"),
    path("wishlist/<int:bookline_id>", wishlist_items, name="wishlist-items"),
    path("wishlist-item/<int:wishlistitem_id>", wishlist_item, name="wishlist-item"),
    path("orders", orders, name="orders"),
    path("create-order", create_order, name="create-order"),
]
