from django.urls import path
from .views import *

urlpatterns = [
    path("cart", get_cart_items, name="cart"),
    path("add/<int:bookline_id>", add_to_cart, name="add"),
]
