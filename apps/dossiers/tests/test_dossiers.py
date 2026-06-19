from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.vehicles.models import Vehicle
from apps.dossiers.models import Dossier


def make_vehicle(**kwargs):
    defaults = {
        'marque': 'Renault', 'modele': 'Clio', 'annee': 2021,
        'kilometrage': 30000, 'prix': '9990.00', 'motorisation': 'essence',
        'couleur': 'Blanc', 'type': 'achat', 'disponible': True,
    }
    defaults.update(kwargs)
    return Vehicle.objects.create(**defaults)


def make_user(email='client@test.fr', **kwargs):
    return User.objects.create_user(
        email=email, password='Pass123!',
        first_name='Marie', last_name='Martin', **kwargs
    )


class DossierClientTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.user = make_user()
        self.vehicle = make_vehicle()
        self.list_url = reverse('dossier-list')
        self.client_api.force_authenticate(user=self.user)

    def test_create_dossier_achat(self):
        data = {'vehicle': self.vehicle.pk, 'type': 'achat', 'message': 'Intéressé par ce véhicule.'}
        response = self.client_api.post(self.list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['statut'], 'en_attente')
        self.assertIn('MM-', response.data['reference'])

    def test_create_dossier_location_with_options(self):
        v = make_vehicle(type='location')
        data = {
            'vehicle': v.pk, 'type': 'location',
            'assurance': True, 'assistance': True,
            'entretien': False, 'controle_technique': True,
        }
        response = self.client_api.post(self.list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['options']['assurance'])
        self.assertFalse(response.data['options']['entretien'])

    def test_list_dossiers_only_own(self):
        # Créer un dossier pour cet utilisateur
        Dossier.objects.create(client=self.user, vehicle=self.vehicle, type='achat')
        # Créer un dossier pour un autre utilisateur
        other = make_user(email='other@test.fr')
        Dossier.objects.create(client=other, vehicle=self.vehicle, type='achat')

        response = self.client_api.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ne voit que son propre dossier
        for d in response.data['results'] if 'results' in response.data else response.data:
            self.assertEqual(d['client']['email'], self.user.email)

    def test_unauthenticated_cannot_access(self):
        anon = APIClient()
        response = anon.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dossier_reference_is_unique(self):
        d1 = Dossier.objects.create(client=self.user, vehicle=self.vehicle, type='achat')
        d2 = Dossier.objects.create(client=self.user, vehicle=self.vehicle, type='achat')
        self.assertNotEqual(d1.reference, d2.reference)

    def test_dossier_detail(self):
        dossier = Dossier.objects.create(client=self.user, vehicle=self.vehicle, type='achat')
        url = reverse('dossier-detail', kwargs={'pk': dossier.pk})
        response = self.client_api.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reference'], dossier.reference)


class DossierAdminTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@m-motors.fr', password='Admin123!',
            first_name='Admin', last_name='Test',
        )
        self.client_obj = make_user()
        self.vehicle = make_vehicle()
        self.dossier = Dossier.objects.create(
            client=self.client_obj, vehicle=self.vehicle, type='achat'
        )
        self.client_api.force_authenticate(user=self.admin)

    def test_admin_list_all_dossiers(self):
        url = reverse('admin-dossier-list')
        response = self.client_api.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(
            response.data['count'] if 'count' in response.data else len(response.data), 1
        )

    def test_admin_valider_dossier(self):
        url = reverse('admin-dossier-valider', kwargs={'pk': self.dossier.pk})
        response = self.client_api.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dossier.refresh_from_db()
        self.assertEqual(self.dossier.statut, 'valide')

    def test_admin_refuser_dossier(self):
        url = reverse('admin-dossier-refuser', kwargs={'pk': self.dossier.pk})
        response = self.client_api.post(url, {'motif': 'Dossier incomplet.'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dossier.refresh_from_db()
        self.assertEqual(self.dossier.statut, 'refuse')
        self.assertEqual(self.dossier.motif_refus, 'Dossier incomplet.')

    def test_admin_en_cours(self):
        url = reverse('admin-dossier-en-cours', kwargs={'pk': self.dossier.pk})
        response = self.client_api.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dossier.refresh_from_db()
        self.assertEqual(self.dossier.statut, 'en_cours')

    def test_non_admin_cannot_access_admin_endpoints(self):
        regular = APIClient()
        regular.force_authenticate(user=self.client_obj)
        url = reverse('admin-dossier-list')
        response = regular.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_dossiers_by_statut(self):
        # Valider ce dossier
        self.dossier.statut = 'valide'
        self.dossier.save()
        # Créer un autre en attente
        Dossier.objects.create(client=self.client_obj, vehicle=self.vehicle, type='achat')

        url = reverse('admin-dossier-list')
        response = self.client_api.get(url, {'statut': 'valide'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        for d in results:
            self.assertEqual(d['statut'], 'valide')
