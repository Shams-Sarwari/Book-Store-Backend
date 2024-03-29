from django.urls import path
from .views import *

urlpatterns = [
    path("cart-items", cart_items, name="cart-items"),  # shows the cart of a user
    path("cart-items/<int:bookline_id>", cart_items, name="cart-items"),
    path("cart-item/<int:cartitem_id>", cart_item, name="cart-item"),
    path("wishlist", wishlist_items, name="wishlist-items"),
    path("wishlist/<int:bookline_id>", wishlist_items, name="wishlist-items"),
    path("wishlist-item/<int:wishlistitem_id>", wishlist_item, name="wishlist-item"),
    path("orders", orders, name="orders"),
    path("orders/<int:order_id>", order, name="order"),
    path("create-order", create_order, name="create-order"),
    path(
        "address/<int:order_id>", address, name="create-order"
    ),  # add address to a order
]
