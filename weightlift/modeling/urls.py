# CONFIGURE API URL
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('video', views.video, name='video')
]