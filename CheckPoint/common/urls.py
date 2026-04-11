from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('website-news/', views.website_news, name='website_news'),
    path('admin-panel/', views.AdminPanelView.as_view(), name='admin page'),
    path('community/', views.community, name='community page'),
    path('events/', views.events, name='community events page'),
    path('events/add/', views.add_event, name='community add event page'),
    path('forums/', views.forum_index, name='forum index'),
    path('forums/new-topic/', views.forum_new_topic, name='forum new topic'),
    path('forums/<str:board_slug>/', views.forum_board, name='forum board'),
    path('forums/<str:board_slug>/<str:thread_slug>/', views.forum_thread, name='forum thread'),
    path('screenshots/', views.screenshots_main, name='screenshots main'),
    path('screenshots/latest/', views.latest_screenshots, name='latest screenshots'),
    path('screenshots/top-rated/', views.top_rated_screenshots, name='top rated screenshots'),
    path('screenshots/upload/', views.upload_screenshot, name='upload screenshot'),
    path('screenshots/my/', views.my_screenshots, name='my screenshots'),
    path('404/', views.custom_404, name='404 page'),
]
