from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from CheckPoint.common.views import CustomAdminLoginView

urlpatterns = [
    path('admin/login/', CustomAdminLoginView.as_view(), name='admin_login'),
    path('admin/', admin.site.urls),
    path('', include('CheckPoint.common.urls'), name='home page'),
    path('accounts/', include('CheckPoint.accounts.urls'), name='accounts page'),
    path('bios/', include('CheckPoint.bios.urls'), name='bios page'),
    path('roms/', include('CheckPoint.roms.urls'), name='roms page'),
    path('saves/', include('CheckPoint.saves.urls'), name='saves page'),
]

# this is so we can serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'CheckPoint.common.views.custom_404'
handler403 = 'CheckPoint.common.views.custom_403'
handler500 = 'CheckPoint.common.views.custom_500'
