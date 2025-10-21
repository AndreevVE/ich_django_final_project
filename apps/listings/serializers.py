from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Listing
from .choices import HOUSING_TYPE_CHOICES


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    housing_type = serializers.ChoiceField(choices=HOUSING_TYPE_CHOICES)

    class Meta:
        model = Listing
        fields = (
            'id', 'title', 'description', 'street', 'city', 'postal_code',
            'price', 'rooms', 'housing_type', 'is_active',
            'created_at', 'updated_at', 'owner'
        )
        read_only_fields = ('owner', 'is_active', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['is_active'] = True
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('owner', None)
        validated_data.pop('is_active', None)
        return super().update(instance, validated_data)
