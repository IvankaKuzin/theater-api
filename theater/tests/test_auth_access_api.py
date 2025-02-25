from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from theater.models import Performance
from theater.serializers import PlayListSerializer, PerformanceListSerializer
from theater.tests.elements_for_tests import *


class UnauthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_genres(self):
        res = self.client.get(GENRES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_required_for_actors(self):
        res = self.client.get(ACTORS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_required_for_plays(self):
        res = self.client.get(PLAYS_URL)

        plays = Play.objects.all().order_by("id")
        serializer = PlayListSerializer(plays, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data["results"])

    def test_auth_required_for_theatre_hall(self):
        res = self.client.get(THEATRE_HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_required_for_reservations(self):
        res = self.client.get(RESERVATIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_performance(self):
        res = self.client.get(PERFORMANCE_URL)

        performances = Performance.objects.all()
        serializer = PerformanceListSerializer(performances, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data["results"])