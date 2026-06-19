from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/vehicles/', include('apps.vehicles.urls')),
    path('api/dossiers/', include('apps.dossiers.urls')),
    path('api/admin/', include('apps.dossiers.admin_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
