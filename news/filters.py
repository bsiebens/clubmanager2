import django_filters
from django.utils.translation import gettext_lazy as _

from .models import NewsItem


class NewsItemFilter(django_filters.FilterSet):
    class Meta:
        model = NewsItem
        fields = ["status", "title"]
