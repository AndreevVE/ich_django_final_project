from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class AuthTests(APITestCase):
    def setUp(self):
        Group.objects.get_or_create(name='Landlords')
        Group.objects.get_or_create(name='Tenants')

    def test_register_tenant(self):
        data = {
            "email": "tenant@example.com",
            "first_name": "Anna",
            "password": "secure123!",
            "password2": "secure123!",
            "role": "tenant"
        }
        response = self.client.post('/api/v1/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="tenant@example.com").exists())
        user = User.objects.get(email="tenant@example.com")
        self.assertTrue(user.groups.filter(name='Tenants').exists())

    def test_register_landlord(self):
        data = {
            "email": "landlord@example.com",
            "first_name": "Max",
            "password": "secure123!",
            "password2": "secure123!",
            "role": "landlord"
        }
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="landlord@example.com")
        self.assertTrue(user.groups.filter(name='Landlords').exists())

    def test_current_user(self):
        user = User.objects.create_user(
            email="test@example.com", first_name="Test", password="pass123"
        )
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "test@example.com")