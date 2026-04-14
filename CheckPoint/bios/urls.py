from django.urls import path
from CheckPoint.bios import views

urlpatterns = [
    path('', views.bios, name='bios page'),
    path('faq/', views.bios_faq, name='bios faq'),
    path('legal/', views.bios_legal, name='bios legal'),
    path('compatibility/', views.bios_comp, name='bios compatibility'),
    path('upload/', views.BiosUploadView.as_view(), name='bios upload'),
    path('all/', views.BiosAllFilesView.as_view(), name='bios all files'),
    path('download/<int:pk>/', views.BiosDownloadView.as_view(), name='bios download'),
    path('delete/<int:pk>/', views.BiosDeleteView.as_view(), name='bios delete'),
]
