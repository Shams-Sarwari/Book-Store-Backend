from django.urls import path
from .views import *

urlpatterns = [
    path("books", book_list, name="books"),
    path("categories", category_list, name="categories"),
    path("categories/<int:category_id>", category_books, name="category-books"),
    path("related-books/<int:pk>", related_books, name="related-books"),
    path("related-booklines/<int:pk>", related_booklines, name="related-booklines"),
    path("<slug:book_slug>/reviews", book_reviews, name="book-reviews"),
    path("reviews/<int:review_id>", review_detail, name="review"),
    path("reviews/<int:review_id>/replies", replies, name="replies"),
    path("replies/<int:reply_id>", reply, name="reply"),
    path("<int:pk>", bookline_detail, name="bookline"),
    path("booklines", bookline_list, name="booklines"),
    path("booklines/<int:book_id>", bookline_list, name="booklines"),
]
