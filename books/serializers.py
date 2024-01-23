from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        

class BookLineSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(source='book.slug')
    book_name = serializers.CharField(source='book.title')
    author_name = serializers.CharField(source='book.author')
    class Meta:
        model = BookLine
        fields = ['id', 'slug', 'book_name','author_name', 'price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'image', 'description']

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author')
    booklines = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'author_name', 'booklines']

    def get_booklines(self, obj):
        first_bookline = obj.booklines.first()
        if first_bookline:
            serialized_data = BookLineSerializer(first_bookline)
            return serialized_data.data
        else:
            return None
        

    