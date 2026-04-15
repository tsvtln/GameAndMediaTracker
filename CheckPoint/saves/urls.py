from django.urls import path
from . import views

urlpatterns = [
    path('', views.saves_main, name='saves main page'),
    path('all/', views.SavesAllView.as_view(), name='saves all page'),
    path('vault/', views.SavesVaultView.as_view(), name='saves vault page'),
    path('upload/', views.SaveUploadView.as_view(), name='saves upload page'),
    path('details/<int:pk>/', views.SaveDetailView.as_view(), name='saves details'),
    path('download/<int:pk>/', views.SaveDownloadView.as_view(), name='saves download'),
    path('delete/<int:pk>/', views.SaveDeleteView.as_view(), name='saves delete'),
    path('vote/<int:pk>/', views.save_vote, name='saves vote'),
]
