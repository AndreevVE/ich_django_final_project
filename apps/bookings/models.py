from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.models import User
from apps.listings.models import Listing
from apps.bookings.choices import BOOKING_STATUS_CHOICES
from apps.common.validators import (
    validate_future_date,
    validate_end_date_after_start,
    validate_booking_duration,
    validate_no_overlapping_booking,
    validate_not_own_listing
)


class Booking(BaseModel):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        verbose_name=_('Объявление'),
        related_name='bookings'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('Арендатор'),
        related_name='bookings'
    )
    start_date = models.DateField(_('Дата начала'), validators=[validate_future_date])
    end_date = models.DateField(_('Дата окончания'))
    check_in_time = models.TimeField(_('Время заезда'), default='14:00')
    check_out_time = models.TimeField(_('Время выезда'), default='12:00')
    total_price = models.DecimalField(
        _('Итоговая цена'),
        max_digits=10,
        decimal_places=2,
        editable=False
    )
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=BOOKING_STATUS_CHOICES,
        default='pending'
    )

    def clean(self):
        if self.start_date and self.end_date:
            validate_end_date_after_start(self.start_date, self.end_date)
            validate_booking_duration(self.start_date, self.end_date)
            if self.tenant and self.listing:
                validate_not_own_listing(self.tenant, self.listing)

                if self.pk is not None:
                    old = Booking.objects.filter(pk=self.pk).first()
                    if old:
                        if old.tenant != self.tenant:
                            raise ValidationError(_("Нельзя изменить арендатора после создания бронирования."))
                        if old.listing != self.listing:
                            raise ValidationError(_("Нельзя изменить объявление после создания бронирования."))
                        if old.start_date != self.start_date or old.end_date != self.end_date:
                            validate_no_overlapping_booking(
                                self.listing, self.start_date, self.end_date, exclude_id=self.pk
                            )
                else:
                    validate_no_overlapping_booking(self.listing, self.start_date, self.end_date)

    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)
        if not skip_validation:
            self.full_clean()
        if self.pk is None or (kwargs.get('update_fields') and
                               any(f in kwargs['update_fields'] for f in ['start_date', 'end_date'])):
            days = (self.end_date - self.start_date).days
            self.total_price = self.listing.price * days
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Бронирование')
        verbose_name_plural = _('Бронирования')
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронь {self.tenant.email} на {self.listing.title} ({self.start_date}–{self.end_date})"


