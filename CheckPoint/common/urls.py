from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('website-news/', views.website_news, name='website_news'),
    path('admin-panel/', views.admin_page, name='admin page'),
    path('community/', views.community, name='community page'),
    path('events/', views.events, name='community events page'),
    path('events/add/', views.add_event, name='community add event page'),
]
