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


class ReplySerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="profile.first_name", read_only=True)
    last_name = serializers.CharField(source="profile.last_name", read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "first_name", "last_name", "comment", "created"]


class ReviewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="profile.first_name", read_only=True)
    last_name = serializers.CharField(source="profile.last_name", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "first_name",
            "last_name",
            "comment",
            "rate",
            "created",
            "replies",
        ]

    def get_replies(self, obj):
        queryset = obj.post_replies.all()[:3]
        serialized_deta = ReplySerializer(queryset, many=True)
        return serialized_deta.data

    def validate_rate(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rate should be between 1 and 5")
        return value
