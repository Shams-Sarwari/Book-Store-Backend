from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        cateogories = Category.objects.all()
        serialized_data = CategorySerializer(cateogories, many=True)
        return Response(serialized_data.data)
    if request.method == 'POST':
        serialized_data = CategorySerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors)
        
@api_view()
def test(request):
    return Response({"message": "welcome"})


@api_view(['GET'])
def book_list(request):
    if request.method == 'GET':
        queryset = Book.objects.all()
        serialized_data = BookSerializer(queryset, many=True)
        return Response(serialized_data.data)


@api_view(['GET'])
def bookline_list(request):
    if request.method == 'GET':
        queryset = BookLine.objects.filter(add_to_page=True)
        serialized_data = BookLineSerializer(queryset, many=True)
        return Response(serialized_data.data)
    
@api_view(['GET'])
def bookline_detail(request, pk):
    queryset = get_object_or_404(BookLine, id=pk)
    if request.method == 'GET':
        serialized_data = BookLineDetailSerializer(queryset)
        return Response(serialized_data.data)

@api_view(['GET'])
def related_books(request, pk):
    category = get_object_or_404(Category, id=pk)
    booklines = BookLine.objects.filter(
        Q(book__category=category) &
        Q(add_to_page=True)
        )
    if len(booklines) < 10:
        queryset = booklines
    else:
        queryset = booklines[0:10]

    serialized_data = BookLineSerializer(queryset, many=True)
    return Response(serialized_data.data)

  
@api_view(['GET'])
def related_booklines(request, pk):
    bookline = get_object_or_404(BookLine, id=pk)
    related_booklines = BookLine.objects.filter(book=bookline.book).exclude(id=bookline.id)

    serialized_data = BookLineSerializer(related_booklines, many=True)
    return Response(serialized_data.data)
