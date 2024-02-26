from books.utils import paginate_items
from datetime import date
from django.db import connection
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Profile, User
from .serializers import (
    ProfileSerializer,
    UserSerializer,
    PasswordChangeSerializer,
    GoogleSocialAuthSerializer,
)


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAdminUser])
def profile_list(request):
    if request.method == "GET":
        queryset = Profile.objects.all()
        queryset = paginate_items(request, queryset, 8)
        serialized_data = ProfileSerializer(queryset, many=True)
        data = Response(serialized_data.data)
        return data


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    if request.method == "GET":
        serialized_data = ProfileSerializer(profile)
        return Response(serialized_data.data)

    if request.method == "PUT":
        serialized_data = ProfileSerializer(profile, data=request.data)
        if serialized_data.is_valid():
            profile = serialized_data.save()
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serialized_data.errors)

    if request.method == "DELETE":
        profile.delete()
        return Response({"message": "successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        serialized_data = UserSerializer(data=request.data)
        data = {}
        if serialized_data.is_valid():
            user = serialized_data.save()
            data["email"] = serialized_data.validated_data["email"]
            data["token"] = get_object_or_404(Token, user=user).key
            return Response(data)
        else:
            return Response(serialized_data.errors)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
        return Response({"message": "You are logged out"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "You are not logged in"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    serialized_data = PasswordChangeSerializer(
        request.user, data=request.data, context={"request": request}
    )
    if serialized_data.is_valid():
        serialized_data.save()
        return Response(
            {"message": "Passwrods changed successfully"}, status=status.HTTP_200_OK
        )
    else:
        return Response(serialized_data.errors)


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def total_users(request):
    previous_users_count = User.objects.exclude(date_joined__date=date.today()).count()
    all_users = User.objects.all().count()
    return Response(
        {
            "previous_users_count": previous_users_count,
            "all_users": all_users,
        },
        status=status.HTTP_200_OK,
    )
