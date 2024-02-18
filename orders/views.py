from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def cart_items(request, bookline_id=None):
    user_cart = get_object_or_404(Cart, profile=request.user.profile)
    if request.method == "GET":
        queryset = CartItem.objects.filter(cart=user_cart)
        serialized_data = CartItemSerializer(queryset, many=True)
        return Response(serialized_data.data)

    if request.method == "POST":
        book_line = get_object_or_404(BookLine, id=bookline_id)
        serialized_data = CartItemSerializer(data=request.data)
        if serialized_data.is_valid():
            # check if the quantity has been sent from the user, if not set 1
            try:
                quantity = serialized_data.validated_data["quantity"]
            except:
                quantity = 1
            # price will automatically set by the multiplication of quantity and item price
            price = quantity * book_line.price

            # first check if the item is already in cart, if so just increase the quantity
            if CartItem.objects.filter(cart=user_cart, book_line=book_line).exists():
                cart_item = CartItem.objects.get(cart=user_cart, book_line=book_line)
                print(cart_item)
                cart_item.quantity += quantity
                cart_item.price += price
                cart_item.save()
            # if the item is not in the cart so add it.
            else:
                serialized_data.save(
                    cart=request.user.profile.cart, book_line=book_line, price=price
                )
            return Response(
                {"message": "successfully added to cart"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serialized_data.errors)


@api_view(["DELETE", "PATCH"])
def cart_item(request, cartitem_id):
    cart_item = get_object_or_404(CartItem, id=cartitem_id)
    if request.method == "DELETE":
        cart_item.delete()
        return Response(
            {"message": "Item deleted successfully"}, status=status.HTTP_200_OK
        )

    if request.method == "PATCH":
        quantity = request.data.get("quantity")
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()
            return Response(
                {"message": "Quantity changed successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Please enter a vlid quantity number"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def wishlist_items(request, bookline_id=None):
    user_wishlist = request.user.profile.wishlist
    if request.method == "GET":
        items = WishlistItem.objects.filter(wishlist=user_wishlist)
        serialized_data = WishlistItemsSerializer(items, many=True)
        return Response(serialized_data.data)

    if request.method == "POST":

        bookline = get_object_or_404(BookLine, id=bookline_id)
        # check if the user has already added item in the wish list
        if bookline.id in WishlistItem.objects.filter(
            wishlist=user_wishlist
        ).values_list("book_line", flat=True):
            return Response(
                {"message": "Item is already in wishlist"}, status=status.HTTP_200_OK
            )
        else:
            WishlistItem.objects.create(wishlist=user_wishlist, book_line=bookline)
            return Response(
                {"message": "Item added successfully"}, status=status.HTTP_201_CREATED
            )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def wishlist_item(reuqest, wishlistitem_id):
    item = get_object_or_404(WishlistItem, id=wishlistitem_id)
    item.delete()
    return Response({"message": "item deleted sucessfully"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def orders(request):
    query = request.query_params.get("filter")
    if query:
        if query == "pending":
            queryset = Order.objects.filter(derlivered=False)
    else:
        queryset = Order.objects.all()
    serialized_data = OrderSerializer(queryset, many=True)
    return Response(serialized_data.data)
