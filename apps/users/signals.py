from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from .apps import UsersConfig
from apps.bookings.models import Booking


# Сигнал для создания групп после миграций
@receiver(post_migrate, sender=UsersConfig)
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Landlords')
    Group.objects.get_or_create(name='Tenants')


# Сигнал для уведомлений о бронировании
# @receiver(post_save, sender=Booking)
# def notify_on_booking(sender, instance, created, **kwargs):
#     if created:
#         landlord = instance.apartment.owner
#         tenant = instance.tenant
#
#         send_mail(
#             subject='Ваша квартира забронирована!',
#             message=f'Пользователь {tenant.email} забронировал вашу квартиру.',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[landlord.email],
#         )
#
#         send_mail(
#             subject='Вы успешно забронировали квартиру!',
#             message='Спасибо за бронирование. Арендодатель скоро свяжется с вами.',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[tenant.email],
#         )