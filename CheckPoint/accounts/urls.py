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
]
