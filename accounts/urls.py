from django.urls import path, include
from .views import *

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("profiles", profile_list, name="profiles"),
    path("profiles/<int:pk>", profile_detail, name="profile"),
    path("messages", contact_messages, name="messages"),
    path("messages/<int:message_id>", message, name="message"),
    path("message-count", number_of_unread_messages, name="message-count"),
    path("register", register_user, name="register"),
    path("login", obtain_auth_token, name="login"),
    path("logout", logout_user, name="logout"),
    path("password-change", change_password, name="password-change"),
    path("google/", GoogleSocialAuthView.as_view()),
    path("user-count", total_users),
]
