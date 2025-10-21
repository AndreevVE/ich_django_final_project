from django.test import TestCase, override_settings
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.listings.models import Listing
from apps.bookings.models import Booking


class ReviewTests(APITestCase):
    def setUp(self):
        Group.objects.get_or_create(name='Landlords')
        Group.objects.get_or_create(name='Tenants')
        self.landlord = User.objects.create_user(email="l@test.com", first_name="L", password="pass123")
        self.landlord.groups.add(Group.objects.get(name='Landlords'))
        self.tenant = User.objects.create_user(email="t@test.com", first_name="T", password="pass123")
        self.tenant.groups.add(Group.objects.get(name='Tenants'))
        self.listing = Listing.objects.create(
            owner=self.landlord, title="Apt", city="Berlin",
            price=100, rooms=1, housing_type='apartment', is_active=True
        )
        # Создаём бронь БЕЗ валидации (для тестов)
        self.booking = Booking(
            listing=self.listing,
            tenant=self.tenant,
            start_date=timezone.now().date() - timezone.timedelta(days=20),
            end_date=timezone.now().date() - timezone.timedelta(days=10),
            status='completed'
        )
        self.booking.save(skip_validation=True)  # ← специальный флаг

    def test_create_review(self):
        self.client.force_authenticate(user=self.tenant)
        data = {
            "booking": self.booking.id,
            "rating": 5,
            "comment": "Great!"
        }
        response = self.client.post(f'/api/v1/listings/{self.listing.id}/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_without_completed_booking_forbidden(self):
        # Создаём НЕзавершённое бронирование БЕЗ валидации
        booking2 = Booking(
            listing=self.listing,
            tenant=self.tenant,
            start_date=timezone.now().date() + timezone.timedelta(days=10),
            end_date=timezone.now().date() + timezone.timedelta(days=12),
            status='pending'
        )
        booking2.save(skip_validation=True)
        self.client.force_authenticate(user=self.tenant)
        data = {"booking": booking2.id, "rating": 5, "comment": "No!"}
        response = self.client.post(f'/api/v1/listings/{self.listing.id}/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)