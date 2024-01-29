from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart_items(request):
    if request.method == "GET":
        queryset = get_object_or_404(Cart, profile=request.user.profile)
        seriazlied_data = CartSerializer(queryset)
        return Response(seriazlied_data.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request, bookline_id):
    if request.method == "POST":
        book_line = get_object_or_404(BookLine, id=bookline_id)
        serialized_data = CartItemSerializer(data=request.data)
        if serialized_data.is_valid():
            try:
                quantity = serialized_data.validated_data["quantity"]
            except:
                quantity = 1
            price = quantity * book_line.price
            serialized_data.save(
                cart=request.user.profile.cart, book_line=book_line, price=price
            )
            return Response(
                {"message": "successfully added to cart"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serialized_data.errors)
