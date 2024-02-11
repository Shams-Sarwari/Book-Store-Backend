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
