from rest_framework import serializers
from .models import *


class ImageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "alt_text", "url"]


class PostSerializer(serializers.ModelSerializer):
    post_images = ImageSerialzier(many=True, read_only=True)
    first_name = serializers.CharField(source="profile.first_name", read_only=True)
    last_name = serializers.CharField(source="profile.last_name", read_only=True)
    slug = serializers.CharField(read_only=True)
    num_of_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "first_name",
            "last_name",
            "title",
            "slug",
            "body",
            "created",
            "post_images",
            "get_rating",
            "num_of_reviews",
        ]

    def get_num_of_reviews(self, obj):
        return len(obj.review_set.filter(active=True))
