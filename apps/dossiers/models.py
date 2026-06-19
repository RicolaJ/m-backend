import uuid
from django.db import models
from django.conf import settings
from apps.vehicles.models import Vehicle


def dossier_document_path(instance, filename):
    return f'dossiers/{instance.dossier.reference}/{filename}'


class Dossier(models.Model):
    TYPE_CHOICES = [('achat', 'Achat'), ('location', 'Location LDA')]
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours d\'instruction'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='dossiers',
        verbose_name='Client',
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name='dossiers',
        verbose_name='Véhicule',
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Type')
    statut = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='en_attente', verbose_name='Statut',
    )
    message = models.TextField(blank=True, verbose_name='Message du client')
    motif_refus = models.TextField(blank=True, verbose_name='Motif de refus')

    # Options location
    assurance = models.BooleanField(default=False, verbose_name='Assurance tous risques')
    assistance = models.BooleanField(default=False, verbose_name='Assistance dépannage')
    entretien = models.BooleanField(default=False, verbose_name='Entretien & SAV')
    controle_technique = models.BooleanField(default=False, verbose_name='Contrôle technique')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dossier'
        verbose_name_plural = 'Dossiers'
        ordering = ['-created_at']

    def __str__(self):
        return f'Dossier {self.reference} — {self.client}'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f'MM-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)


class DossierDocument(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='documents')
    nom = models.CharField(max_length=200, verbose_name='Nom du document')
    fichier = models.FileField(upload_to=dossier_document_path, verbose_name='Fichier')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Document dossier'
        ordering = ['uploaded_at']

    def __str__(self):
        return f'{self.nom} — {self.dossier.reference}'
