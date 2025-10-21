from rest_framework import serializers
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Booking
from apps.common.validators import (
    validate_not_own_listing,
    validate_no_overlapping_booking
)

class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'listing', 'listing_title', 'start_date', 'end_date',
            'check_in_time', 'check_out_time', 'total_price', 'status', 'created_at'
        )
        read_only_fields = ('tenant', 'total_price', 'status', 'created_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            for field in ['start_date', 'end_date', 'check_in_time', 'check_out_time']:
                self.fields[field].read_only = True


    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(_("Требуется авторизация."))

        user = request.user
        start = data['start_date']
        end = data['end_date']
        listing = data['listing']

        validate_not_own_listing(user, listing)
        validate_no_overlapping_booking(listing, start, end)

        return data

    def create(self, validated_data):
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)