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
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password == password2:
            return User.objects.create_user(email=email, password=password)
        else:
            raise serializers.ValidationError("Passwords should be the same")
