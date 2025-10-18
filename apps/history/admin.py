from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SearchQuery, ViewHistory

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'query', 'created_at')
    list_filter = ('created_at', 'is_deleted')
    search_fields = ('query', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description=_('Пользователь'))
    def user_email(self, obj):
        return obj.user.email if obj.user else 'Аноним'

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'listing_title', 'created_at')
    list_filter = ('created_at', 'is_deleted', 'listing__city')
    search_fields = ('user__email', 'listing__title')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('listing',)

    @admin.display(description=_('Пользователь'))
    def user_email(self, obj):
        return obj.user.email if obj.user else 'Аноним'

    @admin.display(description=_('Объявление'))
    def listing_title(self, obj):
        return obj.listing.title