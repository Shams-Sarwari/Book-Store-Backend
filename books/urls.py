from django.urls import path
from .views import *

urlpatterns = [
    path('categories', category_list, name='categories'),
]