from django.urls import path
from .views import *

urlpatterns = [
    path('categories', category_list, name='categories'),
    path('related-books/<int:pk>', related_books, name='related-books'),
    path('books', book_list, name='books'),
    path('<int:pk>', bookline_detail, name='bookline'),
    path('', bookline_list, name='booklines'),

]
