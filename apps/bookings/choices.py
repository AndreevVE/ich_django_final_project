from django.utils.translation import gettext_lazy as _

# Booking status options for tenant-landlord workflow
# Варианты статусов бронирования: ожидающее, подтверждённое, отменённое, завершённое
BOOKING_STATUS_CHOICES = [
    ('pending', _('Pending')),          # Ожидает подтверждения
    ('confirmed', _('Confirmed')),      # Подтверждено
    ('cancelled', _('Cancelled')),      # Отменено
    ('completed', _('Completed')),      # Завершено
]