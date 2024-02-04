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
