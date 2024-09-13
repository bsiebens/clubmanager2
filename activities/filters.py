import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Game


class GameFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter(lookup_expr="gte", label=_("Date"))

    class Meta:
        model = Game
        fields = ["team", "season", "opponent", "date", "competition"]
