from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, Profile
from orders.models import Cart, Wishlist
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
        Cart.objects.create(profile=instance.profile)
        Wishlist.objects.create(profile=instance.profile)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance=None, created=None, **kwargs):
    user = instance.user
    user.delete()
