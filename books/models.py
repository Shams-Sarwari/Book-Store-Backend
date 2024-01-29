from django.db import models
from accounts.models import Profile


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100)
    about = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="cateogry_images")
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, related_name="author_book"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="category_book"
    )
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateField(auto_now_add=True)
    reading_age = models.CharField(max_length=100)
    best_seller = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return self.title

    def get_rating(self):
        reviews = self.review_set.values_list("rate", flat=True)
        num_of_reviews = len(reviews)
        try:
            return sum(reviews) / num_of_reviews
        except:
            return 0


class BookLine(models.Model):
    language = models.CharField(max_length=255)
    translator = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    num_of_pages = models.IntegerField(null=True, blank=True)
    stock_qty = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="booklines")
    add_to_page = models.BooleanField(default=False)
    num_of_views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return f"book line of {self.book.title}"


class Image(models.Model):
    alt_text = models.CharField(max_length=100, blank=True, null=True)
    url = models.ImageField(upload_to="book_images")
    book_line = models.ForeignKey(
        BookLine, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        return f"image for {self.book_line}"


class Review(models.Model):
    comment = models.TextField(blank=True, null=True)
    rate = models.PositiveSmallIntegerField(default=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return str(self.rate)
