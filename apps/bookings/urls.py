from django.urls import path

from .views import BookingListView, BookingDetailView, BookingActionView


# Booking API endpoints: list, detail, and action (e.g., confirm/cancel)
urlpatterns = [
    path("", BookingListView.as_view(), name="booking-list"),  # Список и создание бронирований
    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),  # Получение бронирования
    path("<int:pk>/<str:action>/", BookingActionView.as_view(), name="booking-action"), # Действия с бронированием (cancel/confirm/reject)
]