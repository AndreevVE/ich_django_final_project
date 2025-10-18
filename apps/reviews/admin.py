from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author_email', 'listing_title', 'rating', 'created_at'
    )
    list_filter = ('rating', 'is_deleted', 'created_at', 'booking__listing__city')
    search_fields = (
        'booking__tenant__email', 'booking__listing__title'
    )
    readonly_fields = ('created_at', 'updated_at', 'author_email', 'listing_title')
    autocomplete_fields = ('booking',)

    @admin.display(description=_('Автор'))
    def author_email(self, obj):
        return obj.author.email if obj.author else '—'

    @admin.display(description=_('Объявление'))
    def listing_title(self, obj):
        return obj.listing.title if obj.listing else '—'

    fieldsets = (
        (_('Отзыв'), {
            'fields': ('booking', 'rating', 'comment')
        }),
        (_('Связи (только для чтения)'), {
            'fields': ('author_email', 'listing_title')
        }),
        (_('Системные'), {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )