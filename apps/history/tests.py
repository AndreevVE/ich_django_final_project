# apps/history/tests.py
from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.listings.models import Listing
from .models import SearchQuery, ViewHistory


class HistoryTests(APITestCase):
    def setUp(self):
        Group.objects.get_or_create(name='Landlords')
        Group.objects.get_or_create(name='Tenants')
        self.user = User.objects.create_user(email="u@test.com", first_name="U", password="pass123")
        self.user.groups.add(Group.objects.get(name='Tenants'))
        self.listing = Listing.objects.create(
            owner=self.user, title="Apt", city="Berlin",
            price=100, rooms=1, housing_type='apartment', is_active=True
        )

    def test_search_query_saved(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/listings/?search=berlin')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SearchQuery.objects.count(), 1)
        self.assertEqual(SearchQuery.objects.first().query, 'berlin')

    def test_view_history_saved(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/v1/listings/{self.listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ViewHistory.objects.count(), 1)
        self.assertEqual(ViewHistory.objects.first().listing, self.listing)