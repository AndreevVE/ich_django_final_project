from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.models import User
from apps.listings.models import Listing
from apps.bookings.choices import BOOKING_STATUS_CHOICES



class Booking(BaseModel):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        verbose_name=_('Объявление'),
        related_name='bookings'
    )
    tenant = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Арендатор'),
        related_name='bookings'
    )
    start_date = models.DateField(_('Дата начала'))
    end_date = models.DateField(_('Дата окончания'))
    check_in_time = models.TimeField(_('Время заезда'), default='14:00')
    check_out_time = models.TimeField(_('Время выезда'), default='12:00')
    total_price = models.DecimalField(
        _('Итоговая цена'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
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
            if self.end_date <= self.start_date:
                raise ValidationError(_('Дата окончания должна быть позже даты начала'))
            if self.start_date < timezone.now().date():
                raise ValidationError(_('Нельзя бронировать в прошлом'))

    def save(self, *args, **kwargs):
        # Валидация
        self.full_clean()
        # Рассчитываем total_price ТОЛЬКО при создании
        if self.pk is None:  # ← объект ещё не сохранён в БД
            days = (self.end_date - self.start_date).days
            self.total_price = self.listing.price * days

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Бронирование')
        verbose_name_plural = _('Бронирования')
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронь {self.tenant.email} на {self.listing.title} ({self.start_date}–{self.end_date})"