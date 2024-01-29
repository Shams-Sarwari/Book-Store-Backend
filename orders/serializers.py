from rest_framework import serializers
from books.serializers import BookLineSerializer
from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    book_line = BookLineSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "book_line", "quantity", "price"]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["cart_items"]
