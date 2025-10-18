import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import Group
from faker import Faker
from apps.users.models import User
from apps.listings.models import Listing
from apps.bookings.models import Booking
from apps.reviews.models import Review
from apps.history.models import SearchQuery, ViewHistory

# Немецкая локализация
fake = Faker('de_DE')


class Command(BaseCommand):
    help = 'Заполняет базу данных реалистичными данными по Германии'

    def handle(self, *args, **options):
        self.stdout.write('🧹 Очистка старых данных...')
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        SearchQuery.objects.all().delete()
        ViewHistory.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()

        # === Группы ===
        self.stdout.write('👥 Создание групп...')
        landlord_group, _ = Group.objects.get_or_create(name='Landlords')
        tenant_group, _ = Group.objects.get_or_create(name='Tenants')

        # === Пользователи ===
        self.stdout.write('👤 Создание пользователей (Германия)...')
        landlords = []
        tenants = []

        for _ in range(5):
            user = User.objects.create_user(
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='securepassword123'
            )
            user.groups.add(landlord_group)
            landlords.append(user)

        for _ in range(12):
            user = User.objects.create_user(
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='securepassword123'
            )
            user.groups.add(tenant_group)
            tenants.append(user)

        # === Объявления ===
        self.stdout.write('🏠 Создание объявлений (Германия)...')
        listings = []
        HOUSING_TYPES = ['apartment', 'house', 'studio']
        GERMAN_CITIES = [
            'Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt am Main',
            'Stuttgart', 'Düsseldorf', 'Leipzig', 'Dortmund', 'Essen'
        ]

        for landlord in landlords:
            for _ in range(random.randint(2, 4)):
                listing = Listing.objects.create(
                    title=fake.sentence(nb_words=4)[:-1],
                    description=fake.text(max_nb_chars=300),
                    city=random.choice(GERMAN_CITIES),
                    street=fake.street_address(),
                    postal_code=fake.postcode(),
                    price=round(random.uniform(600, 3500), 2),  # €/месяц
                    rooms=random.randint(1, 4),
                    housing_type=random.choice(HOUSING_TYPES),
                    is_active=True,
                    owner=landlord
                )
                listings.append(listing)

        # === Бронирования ===
        self.stdout.write('📅 Создание бронирований (с временем заезда/выезда)...')
        bookings = []
        today = timezone.now().date()

        for tenant in tenants:
            num_bookings = random.randint(1, 3)
            sampled_listings = random.sample(listings, k=min(num_bookings, len(listings)))
            for listing in sampled_listings:
                # Для сиида временно разрешаем прошлые даты
                start_date = today - timedelta(days=random.randint(1, 60))
                nights = random.randint(3, 21)
                end_date = start_date + timedelta(days=nights)

                booking = Booking(
                    listing=listing,
                    tenant=tenant,
                    start_date=start_date,
                    end_date=end_date,
                    status='completed'
                )
                booking.save(skip_past_check=True)  # обходим проверку
                bookings.append(booking)

        # === Отзывы ===
        self.stdout.write('⭐ Создание отзывов...')
        reviewable_bookings = [b for b in bookings if b.status in ['confirmed', 'completed']]
        for booking in random.sample(reviewable_bookings, k=min(18, len(reviewable_bookings))):
            Review(
                booking=booking,
                rating=random.randint(4, 5),
                comment=fake.text(max_nb_chars=220)
            ).save(skip_booking_check=True)

        # === История ===
        self.stdout.write('🔍 Создание истории поиска и просмотров...')
        for tenant in tenants:
            # Поисковые запросы на немецком
            for _ in range(random.randint(4, 7)):
                SearchQuery.objects.create(
                    user=tenant,
                    query=fake.word().lower()
                )
            # Просмотры
            for listing in random.sample(listings, k=min(6, len(listings))):
                ViewHistory.objects.create(
                    user=tenant,
                    listing=listing
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ База данных успешно заполнена данными по Германии!\n'
                f'   👥 Арендодатели: {len(landlords)}\n'
                f'   👤 Арендаторы: {len(tenants)}\n'
                f'   🏠 Объявлений: {len(listings)}\n'
                f'   📅 Бронирований: {len(bookings)}\n'
                f'   ⭐ Отзывов: {Review.objects.count()}\n'
                f'   💡 Все бронирования имеют время заезда (14:00) и выезда (12:00) по умолчанию.'
            )
        )