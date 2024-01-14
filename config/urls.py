
from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from books.views import test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('', test),
]


