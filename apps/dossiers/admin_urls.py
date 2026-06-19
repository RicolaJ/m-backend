from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminDossierViewSet

router = DefaultRouter()
router.register('dossiers', AdminDossierViewSet, basename='admin-dossier')

urlpatterns = [path('', include(router.urls))]
