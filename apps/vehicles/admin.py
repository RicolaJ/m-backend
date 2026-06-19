from django.contrib import admin
from .models import Vehicle, VehicleImage


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['marque', 'modele', 'annee', 'kilometrage', 'prix', 'type', 'disponible', 'created_at']
    list_filter = ['type', 'motorisation', 'disponible']
    search_fields = ['marque', 'modele']
    list_editable = ['disponible', 'type']
    inlines = [VehicleImageInline]
    ordering = ['-created_at']
