from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.bookings.models import Booking

class Review(BaseModel):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name=_('Бронирование')
    )
    rating = models.PositiveSmallIntegerField(
        _('Рейтинг'),
        validators=[
            MinValueValidator(1, message=_('Рейтинг должен быть от 1 до 5.')),
            MaxValueValidator(5, message=_('Рейтинг должен быть от 1 до 5.'))
        ]
    )
    comment = models.TextField(_('Комментарий'))

    @property
    def listing(self):
        return self.booking.listing

    @property
    def author(self):
        return self.booking.tenant


    def clean(self):
        """
        Проверяем, что:
        - бронирование подтверждено,
        - дата окончания уже прошла (можно оставить отзыв только после проживания).
        """
        booking = self.booking

        # 1. Бронирование должно быть подтверждено или завершено
        if booking.status not in ['confirmed', 'completed']:
            raise ValidationError({
                'booking': _('Можно оставлять отзыв только по подтверждённым или завершённым бронированиям.')
            })

        # 2. Сегодняшняя дата должна быть >= end_date
        if timezone.now().date() < booking.end_date:
            raise ValidationError({
                'booking': _('Нельзя оставить отзыв до окончания срока проживания.')
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # ← запускает clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author.email} на «{self.listing.title}» ({self.rating})"