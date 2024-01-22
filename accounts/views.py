from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.
@api_view(['GET'])
def profile_list(reqeust):
    if reqeust.method == 'GET':
        queryset = Profile.objects.all()
        serialized_data = ProfileSerializer(queryset, many=True)
        return Response(serialized_data.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    if request.method == 'GET':
        serialized_data = ProfileSerializer(profile)
        return Response(serialized_data.data)
    
    if request.method == 'PUT':
        serialized_data = ProfileSerializer(profile, data=request.data)
        if serialized_data.is_valid():
            profile = serialized_data.save()
            return Response({'message': 'successful'}, status=status.HTTP_200_OK)
        else:
            return Response(serialized_data.errors)
        
    if request.method == 'DELETE':
        profile.delete()
        return Response({'message': 'successful'}, status=status.HTTP_200_OK)