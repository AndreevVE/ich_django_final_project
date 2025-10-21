from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal



def validate_future_date(value):
    """Проверяет, что дата не в прошлом."""
    if value < timezone.now().date():
        raise ValidationError(_("Нельзя использовать дату из прошлого."))


def validate_price_range(value, min_price=Decimal('10.00'), max_price=Decimal('10000.00')):
    """Проверка диапазона цены за ночь."""
    if value < min_price:
        raise ValidationError(_("Минимальная цена — %(min)s €.") % {'min': min_price})
    if value > max_price:
        raise ValidationError(_("Максимальная цена — %(max)s €.") % {'max': max_price})


def validate_min_rooms(value):
    """Проверяет, что комнат хотя бы 1."""
    if value < 1:
        raise ValidationError(_("Количество комнат должно быть >= 1."))


def validate_end_date_after_start(start_date, end_date):
    """Проверяет, что дата окончания позже начала."""
    if end_date <= start_date:
        raise ValidationError(_("Дата окончания должна быть позже даты начала."))

def validate_booking_duration(start_date, end_date, min_nights=1, max_nights=365):
    """Проверка минимального и максимального срока бронирования."""
    nights = (end_date - start_date).days
    if nights < min_nights:
        raise ValidationError(_("Минимальный срок бронирования — %(min)s ночей.") % {'min': min_nights})
    if nights > max_nights:
        raise ValidationError(_("Максимальный срок бронирования — %(max)s ночей.") % {'max': max_nights})


def validate_no_overlapping_booking(listing, start_date, end_date, exclude_id=None):
    """Проверяет, что нет пересекающихся активных бронирований."""
    from apps.bookings.models import Booking
    overlapping = Booking.objects.filter(
        listing=listing,
        status__in=['pending', 'confirmed'],
        start_date__lt=end_date,
        end_date__gt=start_date
    )
    if exclude_id:
        overlapping = overlapping.exclude(pk=exclude_id)
    if overlapping.exists():
        raise ValidationError(_("Это жильё уже забронировано на выбранные даты."))


def validate_not_own_listing(user, listing):
    """Проверяет, что пользователь не бронирует своё жильё."""
    if listing.owner == user:
        raise ValidationError(_("Вы не можете забронировать своё собственное жильё."))


def validate_booking_for_review(booking):
    """
    Проверяет, что бронирование можно оставить отзыв:
    - статус confirmed/completed
    - дата окончания в прошлом
    """
    from django.utils import timezone
    from django.core.exceptions import ValidationError
    from django.utils.translation import gettext_lazy as _

    if booking.status not in ['confirmed', 'completed']:
        raise ValidationError(
            _("Можно оставлять отзыв только по подтверждённым или завершённым бронированиям.")
        )

    if timezone.now().date() < booking.end_date:
        raise ValidationError(
            _("Нельзя оставить отзыв до окончания срока проживания.")
        )