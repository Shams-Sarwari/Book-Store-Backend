from django.urls import path
from .views import *

urlpatterns = [
    path('books', book_list, name='books'),
    path('categories', category_list, name='categories'),
    path('related-books/<int:pk>', related_books, name='related-books'),
    path('related-booklines/<int:pk>', related_booklines, name='related-booklines'),
    path('<int:book_id>/reviews', book_reviews, name='book-reviews'),
    path('reviews/<int:review_id>', review_detail, name='review'),
    path('<int:pk>', bookline_detail, name='bookline'),
    path('', bookline_list, name='booklines'),

]
