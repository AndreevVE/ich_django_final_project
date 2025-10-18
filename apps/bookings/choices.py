from django.utils.translation import gettext_lazy as _

BOOKING_STATUS_CHOICES = [
    ('pending', _('Ожидает подтверждения')),
    ('confirmed', _('Подтверждено')),
    ('cancelled', _('Отменено')),
    ('completed', _('Завершено')),
]