from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.models import User
from .choices import HOUSING_TYPE_CHOICES

class Listing(BaseModel):
    title = models.CharField(_('Заголовок'), max_length=255)
    description = models.TextField(_('Описание'))
    street = models.CharField(_('Улица и номер дома'), max_length=255, blank=True)
    city = models.CharField(_('Город'), max_length=100)
    postal_code = models.CharField(_('Почтовый индекс'), max_length=10, blank=True)
    price = models.DecimalField(
        _('Цена'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), message=_('Цена должна быть положительной.'))]
    )
    rooms = models.PositiveSmallIntegerField(
        _('Количество комнат'),
        validators=[
            MinValueValidator(1, message=_('Минимум 1 комната.')),
            MaxValueValidator(10, message=_('Максимум 10 комнат.'))
        ]
    )
    housing_type = models.CharField(_('Тип жилья'), max_length=20, choices=HOUSING_TYPE_CHOICES)
    is_active = models.BooleanField(_('Активно'), default=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Владелец'),
        related_name='listings'
    )

    class Meta:
        verbose_name = _('Объявление')
        verbose_name_plural = _('Объявления')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.city}) — {self.price} "