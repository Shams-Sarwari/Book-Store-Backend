from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    print('inside signal')
    if created:
        Profile.objects.create(user=instance)