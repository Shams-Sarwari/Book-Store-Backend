from django.db.models.signals import post_save, post_delete
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from .models import User, Profile
from orders.models import Cart, Wishlist
from rest_framework.authtoken.models import Token

from django_rest_passwordreset.signals import reset_password_token_created


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


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        "current_user": reset_password_token.user,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse("password_reset:reset-password-confirm")
            ),
            reset_password_token.key,
        ),
    }

    # render email text
    # email_html_message = render_to_string("email/password_reset_email.html", context)
    email_plaintext_message = render_to_string(
        "email/password_reset_email.txt", context
    )

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Your Website Title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@yourdomain.com",
        # to:
        [reset_password_token.user.email],
    )
    # msg.attach_alternative(email_html_message, "text/html")
    msg.send()
