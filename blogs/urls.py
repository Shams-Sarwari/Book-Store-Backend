from django.urls import path
from .views import *

urlpatterns = [
    path("", posts, name="posts"),
    path("<slug:post_slug>", post, name="post"),
]
