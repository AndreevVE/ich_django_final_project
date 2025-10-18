from django.urls import path
from .views import BookingListView, BookingDetailView, BookingActionView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/<str:action>/', BookingActionView.as_view(), name='booking-action'),
]