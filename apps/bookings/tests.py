from django.test import TestCase
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.listings.models import Listing
from .models import Booking


class BookingTests(APITestCase):
    def setUp(self):
        # Создаём группы (они нужны для пермишенов)
        Group.objects.get_or_create(name='Landlords')
        Group.objects.get_or_create(name='Tenants')

        # Создаём пользователей
        self.landlord = User.objects.create_user(
            email="landlord@test.com",
            first_name="Landlord",
            password="securepassword123"
        )
        self.landlord.groups.add(Group.objects.get(name='Landlords'))

        self.tenant = User.objects.create_user(
            email="tenant@test.com",
            first_name="Tenant",
            password="securepassword123"
        )
        self.tenant.groups.add(Group.objects.get(name='Tenants'))

        # Создаём объявление
        self.listing = Listing.objects.create(
            owner=self.landlord,
            title="Уютная квартира",
            city="Berlin",
            price=1200.00,
            rooms=2,
            housing_type='apartment',
            is_active=True
        )

    def test_create_booking(self):
        """Арендатор может создать бронирование."""
        self.client.force_authenticate(user=self.tenant)

        # Даты в будущем
        start_date = timezone.now().date() + timezone.timedelta(days=5)
        end_date = timezone.now().date() + timezone.timedelta(days=7)

        data = {
            "listing": self.listing.id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        response = self.client.post('/api/v1/bookings/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.first()
        self.assertEqual(booking.tenant, self.tenant)
        self.assertEqual(booking.listing, self.listing)
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.start_date, start_date)
        self.assertEqual(booking.end_date, end_date)

    def test_landlord_cannot_book(self):
        """Арендодатель не может создать бронирование."""
        self.client.force_authenticate(user=self.landlord)

        start_date = timezone.now().date() + timezone.timedelta(days=5)
        end_date = timezone.now().date() + timezone.timedelta(days=7)

        data = {
            "listing": self.listing.id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        response = self.client.post('/api/v1/bookings/', data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Booking.objects.count(), 0)