from django.contrib import admin
from .models import Dossier, DossierDocument


class DossierDocumentInline(admin.TabularInline):
    model = DossierDocument
    extra = 0
    readonly_fields = ['uploaded_at']


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ['reference', 'client', 'vehicle', 'type', 'statut', 'created_at']
    list_filter = ['statut', 'type']
    search_fields = ['reference', 'client__email', 'vehicle__marque', 'vehicle__modele']
    readonly_fields = ['reference', 'created_at', 'updated_at']
    list_editable = ['statut']
    inlines = [DossierDocumentInline]
    ordering = ['-created_at']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
