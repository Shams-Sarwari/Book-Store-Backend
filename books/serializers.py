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
    home_image = serializers.SerializerMethodField()
    class Meta:
        model = BookLine
        fields = ['id', 'slug', 'book_name','author_name', 'price', 'home_image']

    def get_home_image(self, obj):
        image = obj.images.first()
        if image:
            return str(image.url)
        else:
            return None
        


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'image', 'description']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ['id', ]

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category_name = serializers.CharField(source='cateogry.title')
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'description','category_name', 'pub_date', 'author', 'num_of_views', 'reading_age']

    
class BookLineDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = BookLine
        fields = ['id','book', 'language', 'translator', 'price', 'stock_qty', 'num_of_pages']
    


    