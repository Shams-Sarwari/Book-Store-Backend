from django.urls import path
from .views import *

urlpatterns = [
    path("", posts, name="posts"),
    path("<slug:post_slug>", post, name="post"),
    path("<slug:post_slug>/reviews", post_reviews, name="reviews"),
    path("reviews/<int:review_id>", review_detail, name="review"),
]
