from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["alt_text", "url"]


class BookLineSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(source="book.slug")
    book_name = serializers.CharField(source="book.title")
    author_name = serializers.CharField(source="book.author")
    home_image = serializers.SerializerMethodField()

    class Meta:
        model = BookLine
        fields = ["id", "slug", "book_name", "author_name", "price", "home_image"]

    def get_home_image(self, obj):
        image = obj.images.first()
        if image:
            return str(image.url)
        else:
            return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "image", "description"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = [
            "id",
        ]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    category_name = serializers.CharField(source="category.title", read_only=True)
    category_id = serializers.IntegerField(source="category.id")
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "category_name",
            "category_id",
            "pub_date",
            "author",
            "reading_age",
            "get_rating",
            "author_id",
        ]


class BookLineDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = BookLine
        fields = [
            "id",
            "book",
            "language",
            "translator",
            "price",
            "stock_qty",
            "num_of_pages",
            "images",
        ]


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
        queryset = obj.replies.all()[:3]
        serialized_deta = ReplySerializer(queryset, many=True)
        return serialized_deta.data

    def validate_rate(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rate should be between 1 and 5")
        return value
