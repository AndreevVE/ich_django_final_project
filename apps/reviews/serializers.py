from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Review
from apps.bookings.models import Booking


class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'booking',
            'listing_title',
            'author_name',
            'rating',
            'comment',
            'created_at'
        )
        read_only_fields = ('created_at',)

    def validate_booking(self, value):
        """Проверяем, что бронирование принадлежит текущему пользователю и завершено."""
        user = self.context['request'].user

        # Проверка: бронирование существует, завершено и принадлежит пользователю
        if not Booking.objects.filter(
            pk=value.pk,
            tenant=user,
            status='completed'
        ).exists():
            raise serializers.ValidationError(_(
                "Оставить отзыв можно только на своё завершённое бронирование."
            ))
        return value

