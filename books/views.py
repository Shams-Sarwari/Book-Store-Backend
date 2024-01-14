from django.shortcuts import render
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
        

