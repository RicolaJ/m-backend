from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.vehicles.models import Vehicle


def make_vehicle(**kwargs):
    defaults = {
        'marque': 'Renault', 'modele': 'Clio', 'annee': 2021,
        'kilometrage': 30000, 'prix': '9990.00', 'motorisation': 'essence',
        'couleur': 'Blanc', 'type': 'achat', 'disponible': True,
    }
    defaults.update(kwargs)
    return Vehicle.objects.create(**defaults)


class VehiclePublicTests(TestCase):
    """Tests sans authentification — lecture seule."""

    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('vehicle-list')
        make_vehicle(type='achat')
        make_vehicle(type='location', loyer_mensuel='199.00')
        make_vehicle(disponible=False)  # Ne doit pas apparaître

    def test_list_vehicles_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Le véhicule indisponible ne doit pas apparaître
        self.assertEqual(response.data['count'], 2)

    def test_filter_by_type_achat(self):
        response = self.client.get(self.list_url, {'type': 'achat'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for v in response.data['results']:
            self.assertEqual(v['type'], 'achat')

    def test_filter_by_type_location(self):
        response = self.client.get(self.list_url, {'type': 'location'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for v in response.data['results']:
            self.assertEqual(v['type'], 'location')

    def test_search_by_marque(self):
        make_vehicle(marque='Peugeot', modele='308')
        response = self.client.get(self.list_url, {'search': 'Peugeot'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['marque'], 'Peugeot')

    def test_get_vehicle_detail(self):
        v = make_vehicle()
        response = self.client.get(reverse('vehicle-detail', kwargs={'pk': v.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['marque'], 'Renault')

    def test_create_vehicle_unauthenticated(self):
        response = self.client.post(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VehicleAdminTests(TestCase):
    """Tests admin — CRUD complet."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@m-motors.fr', password='Admin123!',
            first_name='Admin', last_name='M-Motors',
        )
        self.client.force_authenticate(user=self.admin)
        self.list_url = reverse('vehicle-list')

    def test_create_vehicle_admin(self):
        data = {
            'marque': 'BMW', 'modele': 'Serie 1', 'annee': 2022,
            'kilometrage': 15000, 'prix': '24900.00', 'motorisation': 'essence',
            'couleur': 'Noir', 'type': 'achat',
        }
        response = self.client.post(self.list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vehicle.objects.filter(marque='BMW').exists())

    def test_switch_type(self):
        v = make_vehicle(type='achat')
        url = reverse('vehicle-switch-type', kwargs={'pk': v.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        v.refresh_from_db()
        self.assertEqual(v.type, 'location')

    def test_switch_type_back(self):
        v = make_vehicle(type='location')
        url = reverse('vehicle-switch-type', kwargs={'pk': v.pk})
        self.client.post(url)
        v.refresh_from_db()
        self.assertEqual(v.type, 'achat')

    def test_delete_vehicle(self):
        v = make_vehicle()
        url = reverse('vehicle-detail', kwargs={'pk': v.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehicle.objects.filter(pk=v.pk).exists())

    def test_filter_prix_max(self):
        make_vehicle(prix='5000.00')
        make_vehicle(prix='20000.00')
        response = self.client.get(self.list_url, {'prix__lte': '10000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for v in response.data['results']:
            self.assertLessEqual(float(v['prix']), 10000)
