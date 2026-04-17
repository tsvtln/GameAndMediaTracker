from django.urls import path
from CheckPoint.common import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('website-news/', views.website_news, name='website_news'),
    path('admin-panel/', views.AdminPanelView.as_view(), name='admin page'),
    path('community/', views.community, name='community page'),
    path('events/', views.events, name='community events page'),
    path('events/add/', views.AddEventView.as_view(), name='community add event page'),
    path('events/mark-passed/<int:pk>/', views.mark_event_as_passed, name='event mark passed'),
    path('events/delete/<int:pk>/', views.EventDeleteView.as_view(), name='event delete'),
    path('forums/', views.forum_index, name='forum index'),
    path('forums/new-topic/', views.forum_new_topic, name='forum new topic'),
    path('forums/<str:board_slug>/', views.forum_board, name='forum board'),
    path('forums/<str:board_slug>/<str:thread_slug>/', views.forum_thread, name='forum thread'),
    path('forums/thread/delete/<int:pk>/', views.ThreadDeleteView.as_view(), name='forum thread delete'),
    path('forums/post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='forum post delete'),
    path('screenshots/', views.screenshots_main, name='screenshots main'),
    path('screenshots/latest/', views.latest_screenshots, name='latest screenshots'),
    path('screenshots/top-rated/', views.top_rated_screenshots, name='top rated screenshots'),
    path('screenshots/upload/', views.upload_screenshot, name='upload screenshot'),
    path('404/', views.custom_404, name='404 page'),
    path('403/', views.custom_403, name='403 page'),
    path('500/', views.custom_500, name='500 page'),
]
