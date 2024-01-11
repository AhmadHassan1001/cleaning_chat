from .views import *
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', query_bot, name='query_bot'),
]