from django.urls import path
from . import views

urlpatterns = [
    path('', views.bios, name='bios page'),
    path('faq/', views.bios_faq, name='bios faq'),
    path('legal/', views.bios_legal, name='bios legal'),
    path('compatibility/', views.bios_comp, name='bios compatibility'),
    path('upload/', views.bios_upload, name='bios upload'),
    path('all/', views.bios_all_files, name='bios all files'),
]
