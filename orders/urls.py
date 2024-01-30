from django.urls import path
from .views import *

urlpatterns = [
    path("cart-items", cart_items, name="cart-items"),
    path("cart-items/<int:bookline_id>", cart_items, name="cart-items"),
    path("cart-item/<int:cartitem_id>", cart_item, name="cart-item"),
]
