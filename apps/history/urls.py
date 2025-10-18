from django.urls import path
from .views import PopularSearchView

urlpatterns = [
    path('popular-search/', PopularSearchView.as_view(), name='popular-search'),
]