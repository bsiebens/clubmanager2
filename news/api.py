from rest_framework import viewsets
from django.utils import timezone
from .models import NewsItem
from .serializers import NewsItemSerializer
from rest_framework.pagination import PageNumberPagination


class PaginationClass(PageNumberPagination):
    page_size = 8


class NewsItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsItemSerializer
    queryset = (
        NewsItem.objects.filter(status=NewsItem.StatusChoices.RELEASED, publish_on__lte=timezone.now())
        .exclude(type=NewsItem.NewsItemTypeChoices.INTERNAL)
        .order_by("-publish_on")
    )
    lookup_field = "slug"
    pagination_class = PaginationClass
