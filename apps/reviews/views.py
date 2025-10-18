from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from apps.common.permissions import IsTenant


class ReviewListView(generics.ListCreateAPIView):
    """
    Публичный список отзывов для конкретного объявления.

    - GET: доступен всем (включая анонимов).
    - POST: только арендаторам с завершённым бронированием.
    """
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Только арендаторы могут создавать отзывы
            return [IsTenant()]
        # Отзывы публичные — читать может кто угодно
        return [permissions.AllowAny()]

    def get_queryset(self):
        listing_id = self.kwargs['listing_id']
        return Review.objects.filter(
            booking__listing_id=listing_id,
            is_deleted=False
        )