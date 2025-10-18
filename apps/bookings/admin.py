from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'tenant_email', 'listing_title', 'start_date', 'end_date',
        'check_in_time', 'check_out_time', 'status', 'total_price'
    )
    list_filter = ('status', 'is_deleted', 'start_date', 'end_date', 'listing__city')
    search_fields = (
        'tenant__email', 'listing__title', 'listing__city'
    )
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    autocomplete_fields = ('listing', 'tenant')

    @admin.display(description=_('Арендатор'), ordering='tenant__email')
    def tenant_email(self, obj):
        return obj.tenant.email

    @admin.display(description=_('Объявление'), ordering='listing__title')
    def listing_title(self, obj):
        return obj.listing.title

    fieldsets = (
        (_('Бронирование'), {
            'fields': ('listing', 'tenant', 'status')
        }),
        (_('Даты и время'), {
            'fields': ('start_date', 'end_date', 'check_in_time', 'check_out_time')
        }),
        (_('Цена'), {
            'fields': ('total_price',)
        }),
        (_('Системные'), {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )