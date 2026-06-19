from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Vehicle
from .serializers import VehicleSerializer, VehicleWriteSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.filter(disponible=True).prefetch_related('vehicle_images')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'motorisation', 'disponible']
    search_fields = ['marque', 'modele', 'couleur', 'description']
    ordering_fields = ['prix', 'kilometrage', 'annee', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VehicleWriteSerializer
        return VehicleSerializer

    def get_queryset(self):
        qs = Vehicle.objects.prefetch_related('vehicle_images')
        # Admin sees all; public sees only available
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(disponible=True)
        # Price filter
        prix_max = self.request.query_params.get('prix__lte')
        if prix_max:
            qs = qs.filter(prix__lte=prix_max)
        return qs

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def switch_type(self, request, pk=None):
        """Bascule un véhicule entre achat et location."""
        vehicle = self.get_object()
        vehicle.type = 'location' if vehicle.type == 'achat' else 'achat'
        vehicle.save()
        return Response(VehicleSerializer(vehicle, context={'request': request}).data)
