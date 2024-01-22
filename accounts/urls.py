from django.urls import path
from .views import *

urlpatterns = [
    path('profiles', profile_list, name='profiles'),
    path('profiles/<int:pk>', profile_detail, name='profile'),
]
