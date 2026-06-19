from django.db import models


class Vehicle(models.Model):
    TYPE_CHOICES = [('achat', 'Achat'), ('location', 'Location LDA')]
    MOTORISATION_CHOICES = [
        ('essence', 'Essence'), ('diesel', 'Diesel'),
        ('hybride', 'Hybride'), ('electrique', 'Électrique'),
        ('gpl', 'GPL'),
    ]

    marque = models.CharField(max_length=100, verbose_name='Marque')
    modele = models.CharField(max_length=100, verbose_name='Modèle')
    annee = models.PositiveIntegerField(verbose_name='Année')
    kilometrage = models.PositiveIntegerField(verbose_name='Kilométrage')
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix (€)')
    loyer_mensuel = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        verbose_name='Loyer mensuel (€)'
    )
    motorisation = models.CharField(max_length=20, choices=MOTORISATION_CHOICES, verbose_name='Motorisation')
    couleur = models.CharField(max_length=50, verbose_name='Couleur')
    description = models.TextField(blank=True, verbose_name='Description')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='achat', verbose_name='Type')
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Véhicule'
        verbose_name_plural = 'Véhicules'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.marque} {self.modele} ({self.annee}) — {self.type}'


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_images')
    image = models.ImageField(upload_to='vehicles/', verbose_name='Image')
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = 'Image véhicule'
