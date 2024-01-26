from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("profiles", profile_list, name="profiles"),
    path("profiles/<int:pk>", profile_detail, name="profile"),
    path("login", obtain_auth_token, name="login"),
    path("logout", logout_user, name="logout"),
]
