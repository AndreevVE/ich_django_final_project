from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'city', 'price', 'rooms', 'housing_type',
        'is_active', 'owner', 'created_at'
    )
    list_filter = ('city', 'housing_type', 'is_active', 'is_deleted', 'created_at')
    search_fields = ('title', 'description', 'city', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('owner',)

    fieldsets = (
        (_('Основное'), {
            'fields': ('title', 'description', 'owner', 'is_active')
        }),
        (_('Адрес'), {
            'fields': ('street', 'city', 'postal_code')
        }),
        (_('Характеристики'), {
            'fields': ('price', 'rooms', 'housing_type')
        }),
        (_('Системные'), {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )