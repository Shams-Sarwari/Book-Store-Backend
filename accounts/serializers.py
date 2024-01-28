from rest_framework import serializers
from .models import Profile
from accounts.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "province",
            "district",
            "contact",
            "avatar",
            "created",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        return User.objects.create_user(email=email, password=password)
