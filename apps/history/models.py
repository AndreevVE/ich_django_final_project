from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel
from apps.users.models import User
from apps.listings.models import Listing

class SearchQuery(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Пользователь')
    )
    query = models.CharField(_('Поисковый запрос'), max_length=255)

    class Meta:
        verbose_name = _('Поисковый запрос')
        verbose_name_plural = _('История поиска')
        ordering = ['-created_at']

    def __str__(self):
        user = self.user.email if self.user else "Аноним"
        return f"{user}: {self.query}"

class ViewHistory(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Пользователь')
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        verbose_name=_('Объявление')
    )

    class Meta:
        verbose_name = _('Просмотр объявления')
        verbose_name_plural = _('История просмотров')
        ordering = ['-created_at']

    def __str__(self):
        user = self.user.email if self.user else "Аноним"
        return f"{user} → {self.listing.title}"