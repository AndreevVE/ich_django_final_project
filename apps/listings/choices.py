from django.utils.translation import gettext_lazy as _

# Housing type options for listings: apartment, house, studio
# Варианты типов жилья: квартира, дом, студия
HOUSING_TYPE_CHOICES = [
    ('apartment', _('Apartment')),      # Квартира
    ('house', _('House')),              # Дом
    ('studio', _('Studio')),            # Студия
]