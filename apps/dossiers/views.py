from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Dossier, DossierDocument
from .serializers import DossierSerializer, DossierCreateSerializer, DossierDocumentSerializer


class DossierViewSet(viewsets.ModelViewSet):
    """Client-facing dossier viewset — users see only their own dossiers."""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Dossier.objects.filter(client=self.request.user)\
            .select_related('vehicle', 'client')\
            .prefetch_related('documents', 'vehicle__vehicle_images')

    def get_serializer_class(self):
        if self.action == 'create':
            return DossierCreateSerializer
        return DossierSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    @action(detail=True, methods=['post'], url_path='upload_document')
    def upload_document(self, request, pk=None):
        dossier = self.get_object()
        file = request.FILES.get('file')
        nom = request.data.get('nom', '')
        if not file or not nom:
            return Response({'detail': 'Fichier et nom requis.'}, status=status.HTTP_400_BAD_REQUEST)
        doc = DossierDocument.objects.create(dossier=dossier, nom=nom, fichier=file)
        return Response(
            DossierDocumentSerializer(doc, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class AdminDossierViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin-only viewset to manage all dossiers."""
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DossierSerializer
    filterset_fields = ['statut', 'type']
    search_fields = ['reference', 'client__email', 'client__last_name', 'vehicle__marque']

    def get_queryset(self):
        return Dossier.objects.all()\
            .select_related('vehicle', 'client')\
            .prefetch_related('documents', 'vehicle__vehicle_images')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        dossier = self.get_object()
        dossier.statut = 'valide'
        dossier.save()
        return Response(DossierSerializer(dossier, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def refuser(self, request, pk=None):
        dossier = self.get_object()
        motif = request.data.get('motif', '')
        dossier.statut = 'refuse'
        dossier.motif_refus = motif
        dossier.save()
        return Response(DossierSerializer(dossier, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def en_cours(self, request, pk=None):
        dossier = self.get_object()
        dossier.statut = 'en_cours'
        dossier.save()
        return Response(DossierSerializer(dossier, context={'request': request}).data)
