from rest_framework import serializers
from books.serializers import BookLineSerializer
from .models import *
from accounts.serializers import ProfileSerializer


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


class WishlistItemsSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book_line.book.title", read_only=True)
    language = serializers.CharField(source="book_line.language", read_only=True)
    category = serializers.CharField(source="book_line.book.category", read_only=True)
    price = serializers.CharField(source="book_line.price", read_only=True)

    try:
        image = serializers.ImageField(
            source="book_line.images.first.url", read_only=True
        )
    except:
        image = None

    class Meta:
        model = WishlistItem
        fields = ["id", "book", "language", "category", "price", "image", "book_line"]


class OrderSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
