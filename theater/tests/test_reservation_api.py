from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from theater.serializers import ReservationListSerializer, ReservationDetailsSerializer
from theater.tests.elements_for_tests import *


class ReservationViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="test@test.com", is_staff=True)
        self.client.force_authenticate(self.user)
        self.play = create_play()
        self.theatre_hall = create_theatre_hall()
        self.performance = create_performance(self.play, self.theatre_hall)
        self.reservation = create_reservation(self.user)
        self.ticket = create_ticket(self.reservation, self.performance)

    def test_list_reservations(self):
        response = self.client.get(RESERVATIONS_URL)
        reservations = Reservation.objects.filter(user=self.user)
        serializer = ReservationListSerializer(reservations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_reservation(self):
        url = reverse("theater:reservation-detail", args=[self.reservation.id])
        response = self.client.get(url)
        serializer = ReservationDetailsSerializer(self.reservation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_reservation(self):
        payload = {
            'tickets': [
                {'row': 1, 'seat': 2, 'performance': self.performance.id},
                {'row': 1, 'seat': 3, 'performance': self.performance.id},
            ]
        }
        url = reverse('theater:reservation-list')
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)
        self.assertEqual(Ticket.objects.filter(reservation__user=self.user).count(), 3)

    def test_create_reservation_invalid_ticket(self):
        payload = {
            'tickets': [
                {'row': -1, 'seat': 2, 'performance': self.performance.id},
            ]
        }
        url = reverse('theater:reservation-list')
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
