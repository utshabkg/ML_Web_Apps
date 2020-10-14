# CONFIGURE API URL
from django.urls import path
from .views import weight

urlpatterns = [
    path('api/predict/', weight, name='weight'),
]