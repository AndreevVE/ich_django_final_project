from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.db.models import Count
from .models import Listing
from .serializers import ListingSerializer
from apps.common.permissions import IsLandlord, IsOwner
from apps.history.models import SearchQuery, ViewHistory


class ListingListView(generics.ListCreateAPIView):
    serializer_class = ListingSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            # Только арендодатели могут создавать
            return [IsLandlord()]
        # GET — доступен всем (включая анонимов)
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Listing.objects.filter(is_active=True, is_deleted=False)
        search = self.request.query_params.get('search')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        rooms_min = self.request.query_params.get('rooms_min')
        rooms_max = self.request.query_params.get('rooms_max')
        housing_type = self.request.query_params.get('housing_type')
        city = self.request.query_params.get('city')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
            # Сохраняем поиск ТОЛЬКО для авторизованных
            if self.request.user.is_authenticated:
                SearchQuery.objects.create(user=self.request.user, query=search)

        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if rooms_min:
            queryset = queryset.filter(rooms__gte=rooms_min)
        if rooms_max:
            queryset = queryset.filter(rooms__lte=rooms_max)
        if housing_type:
            queryset = queryset.filter(housing_type=housing_type)
        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset

    def perform_create(self, serializer):
        # Владелец назначается автоматически
        serializer.save(owner=self.request.user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.filter(is_deleted=False)
    serializer_class = ListingSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Редактирование/удаление — только владелец
            return [IsOwner()]
        # Просмотр — всем
        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Сохраняем просмотр ТОЛЬКО для авторизованных
        if request.user.is_authenticated:
            ViewHistory.objects.get_or_create(user=request.user, listing=instance)
        return super().retrieve(request, *args, **kwargs)


class PopularListingsView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]  # публичный эндпоинт

    def get_queryset(self):
        return Listing.objects.filter(
            is_active=True,
            is_deleted=False
        ).annotate(
            views_count=Count('viewhistory')
        ).order_by('-views_count')[:10]