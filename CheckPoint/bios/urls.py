from django.urls import path
from . import views

urlpatterns = [
    path('', views.bios, name='bios page'),
]
