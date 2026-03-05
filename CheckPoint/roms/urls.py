from django.urls import path
from . import views

urlpatterns = [
    path('', views.roms, name='roms page'),
]
