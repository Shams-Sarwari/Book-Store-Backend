
from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from books.views import test
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', test),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
