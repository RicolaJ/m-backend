from rest_framework import serializers
from .models import Dossier, DossierDocument
from apps.vehicles.serializers import VehicleSerializer
from apps.accounts.serializers import UserSerializer


class DossierDocumentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = DossierDocument
        fields = ['id', 'nom', 'url', 'uploaded_at']

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.fichier.url)
        return obj.fichier.url


class DossierOptionsSerializer(serializers.Serializer):
    assurance = serializers.BooleanField()
    assistance = serializers.BooleanField()
    entretien = serializers.BooleanField()
    controle_technique = serializers.BooleanField()


class DossierSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    documents = DossierDocumentSerializer(many=True, read_only=True)
    options = serializers.SerializerMethodField()

    class Meta:
        model = Dossier
        fields = [
            'id', 'reference', 'client', 'vehicle', 'type', 'statut',
            'message', 'motif_refus', 'options', 'documents',
            'created_at', 'updated_at',
        ]

    def get_options(self, obj):
        if obj.type == 'location':
            return {
                'assurance': obj.assurance,
                'assistance': obj.assistance,
                'entretien': obj.entretien,
                'controle_technique': obj.controle_technique,
            }
        return None


class DossierCreateSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=__import__('apps.vehicles.models', fromlist=['Vehicle']).Vehicle.objects.all()
    )

    class Meta:
        model = Dossier
        fields = [
            'vehicle', 'type', 'message',
            'assurance', 'assistance', 'entretien', 'controle_technique',
        ]

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)
