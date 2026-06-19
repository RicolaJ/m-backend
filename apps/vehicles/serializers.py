from rest_framework import serializers
from .models import Vehicle, VehicleImage


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'ordre']


class VehicleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            'id', 'marque', 'modele', 'annee', 'kilometrage',
            'prix', 'loyer_mensuel', 'motorisation', 'couleur',
            'description', 'type', 'disponible', 'images', 'created_at',
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.vehicle_images.all()
        if request:
            return [request.build_absolute_uri(img.image.url) for img in images]
        return [img.image.url for img in images]


class VehicleWriteSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Vehicle
        fields = [
            'marque', 'modele', 'annee', 'kilometrage', 'prix',
            'loyer_mensuel', 'motorisation', 'couleur', 'description',
            'type', 'disponible', 'uploaded_images',
        ]

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images', [])
        vehicle = Vehicle.objects.create(**validated_data)
        for i, img in enumerate(images):
            VehicleImage.objects.create(vehicle=vehicle, image=img, ordre=i)
        return vehicle

    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', [])
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if images:
            instance.vehicle_images.all().delete()
            for i, img in enumerate(images):
                VehicleImage.objects.create(vehicle=instance, image=img, ordre=i)
        return instance
