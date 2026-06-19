from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import apps.dossiers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(editable=False, max_length=20, unique=True)),
                ('type', models.CharField(
                    choices=[('achat', 'Achat'), ('location', 'Location LDA')],
                    max_length=10, verbose_name='Type'
                )),
                ('statut', models.CharField(
                    choices=[
                        ('en_attente', 'En attente'),
                        ('en_cours', "En cours d'instruction"),
                        ('valide', 'Validé'),
                        ('refuse', 'Refusé'),
                    ],
                    default='en_attente', max_length=20, verbose_name='Statut'
                )),
                ('message', models.TextField(blank=True, verbose_name='Message du client')),
                ('motif_refus', models.TextField(blank=True, verbose_name='Motif de refus')),
                ('assurance', models.BooleanField(default=False, verbose_name='Assurance tous risques')),
                ('assistance', models.BooleanField(default=False, verbose_name='Assistance dépannage')),
                ('entretien', models.BooleanField(default=False, verbose_name='Entretien & SAV')),
                ('controle_technique', models.BooleanField(default=False, verbose_name='Contrôle technique')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='dossiers',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Client',
                )),
                ('vehicle', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='dossiers',
                    to='vehicles.vehicle',
                    verbose_name='Véhicule',
                )),
            ],
            options={
                'verbose_name': 'Dossier',
                'verbose_name_plural': 'Dossiers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DossierDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, verbose_name='Nom du document')),
                ('fichier', models.FileField(upload_to=apps.dossiers.models.dossier_document_path, verbose_name='Fichier')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('dossier', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='documents',
                    to='dossiers.dossier',
                )),
            ],
            options={
                'verbose_name': 'Document dossier',
                'ordering': ['uploaded_at'],
            },
        ),
    ]
