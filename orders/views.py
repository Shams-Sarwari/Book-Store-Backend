from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import is_cart_owner, is_wishlist_owner


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def cart_items(request, bookline_id=None):
    user_cart = get_object_or_404(Cart, profile=request.user.profile)
    if request.method == "GET":
        queryset = (
            CartItem.objects.filter(cart=user_cart)
            .select_related("book_line")
            .select_related("book_line__book")
            .select_related("book_line__book__author")
        )

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
            # the qunatity shouldn't be greater stock qty
            if quantity > book_line.stock_qty:
                return Response(
                    {"error": "the inserted quantity is greated than stock quantity"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
@is_cart_owner
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
            quantity = int(quantity)
        if quantity:
            if quantity > cart_item.book_line.stock_qty:
                return Response(
                    {"error": "The insereted number is greated than stock quantity"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
        items = (
            WishlistItem.objects.filter(wishlist=user_wishlist)
            .select_related("book_line")
            .select_related("book_line__book")
            .select_related("book_line__book__category")
        )
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
@is_wishlist_owner
def wishlist_item(reuqest, wishlistitem_id):
    item = get_object_or_404(WishlistItem, id=wishlistitem_id)
    item.delete()
    return Response({"message": "item deleted sucessfully"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def orders(request):
    query = request.query_params.get("filter")
    if query:
        if query == "pending":
            queryset = Order.objects.filter(derlivered=False)
    else:
        queryset = (
            Order.objects.all().select_related("profile").prefetch_related("address")
        )
    serialized_data = OrderSerializer(queryset, many=True)
    return Response(serialized_data.data)


@api_view(["GET", "PATCH"])
@permission_classes([IsAdminUser])
def order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "GET":
        serialized_data = OrderSerializer(order)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        query = request.query_params.get("status")
        if query == "delivered":
            order.derlivered = True
            order.save()
            return Response(
                {"message": "order marked as delivered"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    cart_items = request.user.profile.cart.cart_items.all()
    if request.method == "POST":
        if cart_items.exists():
            # check if the quantity of items in tha cart are less than stock qty
            for item in cart_items:
                if item.quantity > item.book_line.stock_qty:
                    return Response(
                        {
                            "error": f"{item.book_line.book.title} quantity is more than stock quantity"
                        }
                    )

            # create an order for the user and add order items based on cart items.
            order = Order.objects.create(profile=request.user.profile)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book_line=item.book_line,
                    quantity=item.quantity,
                    price=item.price,
                )
                # change the total price of order based on order items
                order.total_price += item.price
                # reduce quantity of stock with each order
                item.book_line.stock_qty -= item.quantity
                # check if the stock quantity of a book line is 0 so remove for page
                if item.book_line.stock_qty <= 0:
                    item.active = False
                item.book_line.save()
                item.delete()
            order.save()

            return Response(
                {"message": "Order created"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "No item in the cart"}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def address(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        serialized_data = AddressSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save(order=order)
            return Response(
                {"message": "Address added to order"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serialized_data.errors)
