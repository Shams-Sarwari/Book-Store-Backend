from django.urls import path
from .views import *

urlpatterns = [
    path('categories', category_list, name='categories'),
    path('books', book_list, name='books'),
    path('', bookline_list, name='book-lines'),

]
