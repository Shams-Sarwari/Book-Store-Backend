from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


import os


def register_social_user(email, provider):
    filtered_users = User.objects.filter(email=email)
    if filtered_users.exists():
        if provider == filtered_users[0].provider:
            registered_user = authenticate(
                email=email, passowrd=os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
            )

            return {
                "email": registered_user.email,
            }

        else:
            raise AuthenticationFailed(
                detail=f"Please continue your logging in using {filtered_users[0].email}"
            )

    else:
        user = {
            "email": email,
            "password": os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"),
            "provider": "google",
        }
        user = User.objects.create(**user)
        return {
            "email": user.email,
        }
