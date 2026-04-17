from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts page'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('logout/', views.AppUserLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile edit'),
    path('profile/change-password/', views.PasswordChangeView.as_view(), name='change password'),
    path('favorites/', views.FavoritesView.as_view(), name='accounts favorites page'),
    path('favorites/roms/', views.FavoriteRomsView.as_view(), name='accounts favorite roms page'),
    path('favorites/screenshots/', views.FavoriteScreenshotsView.as_view(), name='accounts favorite screenshots page'),
    path('profile/<int:pk>/', views.PublicProfileView.as_view(), name='public profile'),

    # Screenshot URLs
    path('screenshots/', views.ScreenshotListView.as_view(), name='screenshots main'),
    path('screenshots/latest/', views.LatestScreenshotsView.as_view(), name='latest screenshots'),
    path('screenshots/top-rated/', views.TopRatedScreenshotsView.as_view(), name='top rated screenshots'),
    path('screenshots/my/', views.MyScreenshotsView.as_view(), name='my screenshots'),
    path('screenshots/upload/', views.ScreenshotUploadView.as_view(), name='upload screenshot'),
    path('screenshots/delete/<int:pk>/', views.ScreenshotDeleteView.as_view(), name='delete screenshot'),
    path('screenshots/check-favorite/<int:pk>/', views.check_favorite_screenshot, name='check favorite screenshot'),
    path('screenshots/favorite/<int:pk>/', views.toggle_favorite_screenshot, name='toggle favorite screenshot'),
]
