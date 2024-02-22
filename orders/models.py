from django.db import models
from accounts.models import Profile
from books.models import BookLine


# Create your models here.
class Cart(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.profile)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    book_line = models.ForeignKey(BookLine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Wishlist(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.profile)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="wishlistitems"
    )
    book_line = models.ForeignKey(BookLine, on_delete=models.CASCADE)


class Order(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    derlivered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]

    def __str__(self) -> str:
        return f"order of {self.profile}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book_line = models.ForeignKey(BookLine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"order item for {self.order}"


class Address(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    apartment_num = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.city} | {self.country}"
