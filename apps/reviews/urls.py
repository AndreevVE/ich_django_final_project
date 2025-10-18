from django.urls import path
from .views import ReviewListView

urlpatterns = [
    path('listings/<int:listing_id>/reviews/', ReviewListView.as_view(), name='review-list'),
]