from .views import *
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', AgentView.as_view(), name='query_bot'),
]