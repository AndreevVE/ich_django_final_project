from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.bookings.models import Booking
from apps.reviews.models import Review


@receiver(post_save, sender=Booking)
def send_booking_notifications(sender, instance, created, **kwargs):
    """Отправка уведомлений при создании или изменении бронирования."""
    if created:
        # Арендатору: "Вы забронировали"
        send_mail(
            subject=_('Ваше бронирование подтверждено — %(title)s') % {'title': instance.listing.title},
            message=_('Здравствуйте, %(first_name)s!\n\n'
                      'Вы успешно забронировали жильё "%(title)s" '
                      'с %(start_date)s по %(end_date)s.\n\n'
                      'Спасибо за использование %(site_name)s!') % {
                'first_name': instance.tenant.first_name,
                'title': instance.listing.title,
                'start_date': instance.start_date,
                'end_date': instance.end_date,
                'site_name': settings.SITE_NAME
            },
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.tenant.email],
            fail_silently=True
        )

        # Арендодателю: "Ваше объявление забронировали"
        send_mail(
            subject=_('Новое бронирование — %(title)s') % {'title': instance.listing.title},
            message=_('Здравствуйте, %(first_name)s!\n\n'
                      'Пользователь %(tenant_email)s забронировал ваше объявление '
                      '"%(title)s" с %(start_date)s по %(end_date)s.\n\n'
                      'Пожалуйста, подтвердите бронирование в личном кабинете.') % {
                'first_name': instance.listing.owner.first_name,
                'tenant_email': instance.tenant.email,
                'title': instance.listing.title,
                'start_date': instance.start_date,
                'end_date': instance.end_date
            },
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.listing.owner.email],
            fail_silently=True
        )

    elif instance.status == 'confirmed' and 'status' in (kwargs.get('update_fields') or []):
        send_mail(
            subject=_('Бронирование подтверждено — %(title)s') % {'title': instance.listing.title},
            message=_('Здравствуйте, %(first_name)s!\n\n'
                      'Арендодатель подтвердил ваше бронирование '
                      '"%(title)s" с %(start_date)s по %(end_date)s.\n\n'
                      'Добро пожаловать!') % {
                'first_name': instance.tenant.first_name,
                'title': instance.listing.title,
                'start_date': instance.start_date,
                'end_date': instance.end_date
            },
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.tenant.email],
            fail_silently=True
        )

    elif instance.status == 'cancelled' and 'status' in (kwargs.get('update_fields') or []):
        send_mail(
            subject=_('Бронирование отменено'),
            message=_('Бронирование на "%(title)s" было отменено.') % {'title': instance.listing.title},
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.tenant.email],
            fail_silently=True
        )
        send_mail(
            subject=_('Бронирование отменено'),
            message=_('Бронирование на ваше объявление "%(title)s" было отменено.') % {'title': instance.listing.title},
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.listing.owner.email],
            fail_silently=True
        )


@receiver(post_save, sender=Review)
def send_review_notification(sender, instance, created, **kwargs):
    """Уведомление арендодателю о новом отзыве."""
    if created:
        send_mail(
            subject=_('Новый отзыв — %(title)s') % {'title': instance.listing.title},
            message=_('Здравствуйте, %(first_name)s!\n\n'
                      'Арендатор оставил отзыв на ваше объявление "%(title)s":\n\n'
                      'Оценка: %(rating)s ★\n'
                      'Комментарий: %(comment)s\n\n'
                      'Спасибо за вашу работу!') % {
                'first_name': instance.listing.owner.first_name,
                'title': instance.listing.title,
                'rating': instance.rating,
                'comment': instance.comment
            },
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.listing.owner.email],
            fail_silently=True
        )