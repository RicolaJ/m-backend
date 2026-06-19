from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=100, verbose_name='Marque')),
                ('modele', models.CharField(max_length=100, verbose_name='Modèle')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('kilometrage', models.PositiveIntegerField(verbose_name='Kilométrage')),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix (€)')),
                ('loyer_mensuel', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Loyer mensuel (€)')),
                ('motorisation', models.CharField(
                    choices=[('essence', 'Essence'), ('diesel', 'Diesel'), ('hybride', 'Hybride'), ('electrique', 'Électrique'), ('gpl', 'GPL')],
                    max_length=20, verbose_name='Motorisation'
                )),
                ('couleur', models.CharField(max_length=50, verbose_name='Couleur')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('type', models.CharField(
                    choices=[('achat', 'Achat'), ('location', 'Location LDA')],
                    default='achat', max_length=10, verbose_name='Type'
                )),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponible')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Véhicule',
                'verbose_name_plural': 'Véhicules',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VehicleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='vehicles/', verbose_name='Image')),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_images', to='vehicles.vehicle')),
            ],
            options={
                'verbose_name': 'Image véhicule',
                'ordering': ['ordre'],
            },
        ),
    ]
