"""
Management command pour créer un superuser automatiquement au déploiement.
Usage : python manage.py create_superuser_env

Variables d'environnement requises :
  DJANGO_SUPERUSER_EMAIL
  DJANGO_SUPERUSER_PASSWORD
  DJANGO_SUPERUSER_FIRST_NAME (optionnel, défaut: Admin)
  DJANGO_SUPERUSER_LAST_NAME  (optionnel, défaut: M-Motors)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée un superuser depuis les variables d\'environnement'

    def handle(self, *args, **options):
        email = config('DJANGO_SUPERUSER_EMAIL', default='')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='')
        first_name = config('DJANGO_SUPERUSER_FIRST_NAME', default='Admin')
        last_name = config('DJANGO_SUPERUSER_LAST_NAME', default='M-Motors')

        if not email or not password:
            self.stdout.write(self.style.WARNING(
                'DJANGO_SUPERUSER_EMAIL et DJANGO_SUPERUSER_PASSWORD non définis. Skipping.'
            ))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Superuser {email} existe déjà.'))
            return

        User.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser {email} créé avec succès.'))
