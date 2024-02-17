from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile
from accounts.models import User
from .register import register_social_user

import google
import os


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


class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["password", "password2", "old_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"error": "passwords should be the same"})

        return attrs

    def validate_old_password(self, value):

        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"error": "Your old passowrd is not correct"}
            )

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data["sub"]
        except:
            raise serializers.ValidationError("The token is invalid or expired")

        if user_data["aud"] != os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"):
            raise AuthenticationFailed("oops who are you?")

        user_id = user_data["sub"]
        user_email = user_data["email"]
        provider = "google"

        return register_social_user(email=user_email, provider=provider)
