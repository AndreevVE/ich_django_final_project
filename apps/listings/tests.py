from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from .models import Listing


class ListingTests(APITestCase):
    def setUp(self):
        Group.objects.get_or_create(name='Landlords')
        Group.objects.get_or_create(name='Tenants')
        self.landlord = User.objects.create_user(
            email="landlord@test.com", first_name="L", password="pass123"
        )
        self.landlord.groups.add(Group.objects.get(name='Landlords'))
        self.tenant = User.objects.create_user(
            email="tenant@test.com", first_name="T", password="pass123"
        )
        self.tenant.groups.add(Group.objects.get(name='Tenants'))

    def test_listings_public(self):
        Listing.objects.create(
            owner=self.landlord, title="Test", city="Berlin",
            price=1000, rooms=1, housing_type='apartment', is_active=True
        )
        response = self.client.get('/api/v1/listings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_listing_landlord(self):
        self.client.force_authenticate(user=self.landlord)
        data = {
            "title": "New Apt",
            "description": "Nice",
            "city": "Munich",
            "price": 1500,
            "rooms": 2,
            "housing_type": "apartment"
        }
        response = self.client.post('/api/v1/listings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(Listing.objects.first().owner, self.landlord)

    def test_create_listing_tenant_forbidden(self):
        self.client.force_authenticate(user=self.tenant)
        data = {"title": "X", "city": "B", "price": 1000, "rooms": 1, "housing_type": "apartment"}
        response = self.client.post('/api/v1/listings/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)