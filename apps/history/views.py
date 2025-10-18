from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import SearchQuery
from .serializers import PopularSearchSerializer


class PopularSearchView(generics.GenericAPIView):
    """
    Возвращает топ-10 популярных поисковых запросов за последние 30 дней.
    Учитываются только непустые запросы длиной от 3 символов.
    Исключаются мягко удалённые записи.
    """
    serializer_class = PopularSearchSerializer

    def get(self, request, *args, **kwargs):
        since = timezone.now() - timedelta(days=30)

        queryset = (
            SearchQuery.objects
            .filter(
                is_deleted=False,
                created_at__gte=since,
                query__isnull=False,
                query__length__gt=2
            )
            .exclude(query='')
            .values('query')
            .annotate(count=Count('query'))
            .order_by('-count')[:10]
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)