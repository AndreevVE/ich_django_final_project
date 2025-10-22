from django.urls import path

from .views import ListingListView, ListingDetailView,PopularListingsView


# URL patterns for listing management: list/create, detail, and popular listings
urlpatterns = [
    path("", ListingListView.as_view(), name="listing-list"),  # Список и создание объявлений
    path("<int:pk>/", ListingDetailView.as_view(), name="listing-detail"), # Получение, обновление или удаление объявления
    path("popular/", PopularListingsView.as_view(), name="popular-listings"),  # Получение популярных объявлений
]