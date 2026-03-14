from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts page'),
    path('favorites/', views.favorites_page, name='accounts favorites page'),
    path('favorites/roms', views.favorite_roms, name='accounts favorite roms page'),
    path('favorites/screenshots', views.favorite_screenshots, name='accounts favorite screenshots page'),
]
