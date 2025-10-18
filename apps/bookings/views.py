from rest_framework import generics, status, permissions
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Booking
from .serializers import BookingSerializer
from apps.common.permissions import IsTenant, IsBookingOwnerOrLandlord

class BookingListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(
            is_deleted=False
        ).filter(
            Q(tenant=user) | Q(listing__owner=user)
        )
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTenant()]
        return [permissions.IsAuthenticated()]


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.filter(is_deleted=False)
    serializer_class = BookingSerializer
    permission_classes = [IsBookingOwnerOrLandlord]


class BookingActionView(generics.UpdateAPIView):
    queryset = Booking.objects.filter(is_deleted=False)
    serializer_class = BookingSerializer
    permission_classes = [IsBookingOwnerOrLandlord]

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        action = self.kwargs.get('action')
        today = timezone.now().date()

        if action == 'cancel':
            if booking.tenant != request.user:
                return Response(
                    {'error': _('Только арендатор может отменить бронирование.')},
                    status=status.HTTP_403_FORBIDDEN
                )
            if booking.start_date < today + timedelta(days=7):
                return Response(
                    {'error': _('Отмена бронирования возможна не позднее чем за 7 дней до даты начала.')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            booking.status = 'cancelled'

        elif action == 'confirm':
            if booking.listing.owner != request.user:
                return Response(
                    {'error': _('Только арендодатель может подтвердить бронирование.')},
                    status=status.HTTP_403_FORBIDDEN
                )
            booking.status = 'confirmed'

        elif action == 'reject':
            if booking.listing.owner != request.user:
                return Response(
                    {'error': _('Только арендодатель может отклонить бронирование.')},
                    status=status.HTTP_403_FORBIDDEN
                )
            booking.status = 'cancelled'

        else:
            return Response(
                {'error': _('Недопустимое действие. Используйте: cancel, confirm, reject.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.save(update_fields=['status'])
        serializer = self.get_serializer(booking)
        return Response(serializer.data)