from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255,blank=True, null=True)
    country = models.CharField(max_length=100)
    about = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/cateogry_images')
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='author_book')
    cateogry = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category_book')
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateField(auto_now_add=True)
    num_of_views = models.IntegerField(default=0)
    reading_age = models.CharField(max_length=100)
    best_seller = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class BookLine(models.Model):
    language = models.CharField(max_length=255)
    translator = models.CharField(max_length=255,blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_qty = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'book line of {self.book.title}'


class Image(models.Model):
    alt_text = models.CharField(max_length=100,blank=True, null=True)
    url = models.ImageField(upload_to='media/book_images')
    book_line = models.ForeignKey(BookLine, on_delete=models.CASCADE)
