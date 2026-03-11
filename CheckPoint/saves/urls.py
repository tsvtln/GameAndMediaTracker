from django.urls import path
from . import views

urlpatterns = [
    path('', views.saves_main, name='saves main page'),
    path('all/', views.saves_all, name='saves all page'),
    path('vault/', views.vault, name='saves vault page'),
    path('upload/', views.saves_upload, name='saves upload page'),
    path('details/', views.saves_details, name='saves details'),
]
