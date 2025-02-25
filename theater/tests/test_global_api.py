from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

RESERVATIONS_URL = reverse("theater:reservation-list")
PERFORMANCE_URL = reverse("theater:performance-list")

class UnauthenticatedReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESERVATIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.get(PERFORMANCE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)