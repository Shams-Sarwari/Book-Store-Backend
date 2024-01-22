from django.db import models
from accounts.models import Profile
from books.models import BookLine

# Create your models here.
class Cart(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book_line = models.ForeignKey(BookLine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2)