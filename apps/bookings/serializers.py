from rest_framework import serializers
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'listing',
            'listing_title',
            'start_date',
            'end_date',
            'check_in_time',
            'check_out_time',
            'total_price',
            'status',
            'created_at'
        )
        read_only_fields = ('tenant', 'total_price', 'status', 'created_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Запрещаем изменять даты и время после создания брони
        if self.instance:
            self.fields['start_date'].read_only = True
            self.fields['end_date'].read_only = True
            self.fields['check_in_time'].read_only = True
            self.fields['check_out_time'].read_only = True

    def validate_listing(self, value):
        """Проверяем, что объявление активно и не удалено."""
        if not value.is_active or value.is_deleted:
            raise serializers.ValidationError(
                _("Это объявление недоступно для бронирования.")
            )
        return value

    def validate(self, data):
        """Основная бизнес-валидация."""
        user = self.context['request'].user
        start = data['start_date']
        end = data['end_date']
        listing = data['listing']

        # 1. Запрет бронировать своё жильё
        if listing.owner == user:
            raise serializers.ValidationError(
                _("Вы не можете забронировать своё собственное жильё.")
            )

        # 2. Дата начала не в прошлом
        if start < timezone.now().date():
            raise serializers.ValidationError(
                _("Нельзя бронировать в прошлом.")
            )

        # 3. Дата окончания позже начала
        if end <= start:
            raise serializers.ValidationError(
                _("Дата окончания должна быть позже даты начала.")
            )

        # 4. Проверка пересечения с другими бронями
        overlapping = Booking.objects.filter(
            listing=listing,
            status__in=['pending', 'confirmed'],
            start_date__lt=end,
            end_date__gt=start
        )
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        if overlapping.exists():
            raise serializers.ValidationError(
                _("Это жильё уже забронировано на выбранные даты.")
            )

        return data

    def create(self, validated_data):
        """Автоматически назначаем арендатора — текущего пользователя."""
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)