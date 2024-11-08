#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

import django_filters
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from finance.models import OrderForm, Order


class OrderFormFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Name"))

    class Meta:
        model = OrderForm
        fields = ["name", "start_date", "end_date"]


class OrderFilter(django_filters.FilterSet):
    lineitems__member__user__first_name = django_filters.CharFilter(lookup_expr="icontains", label=_("First Name"), distinct=True)
    lineitems__member__user__last_name = django_filters.CharFilter(lookup_expr="icontains", label=_("First Name"), distinct=True)
    start_date = django_filters.DateFilter(lookup_expr="gte", label=_("Start Date"), field_name="created")
    end_date = django_filters.DateFilter(lookup_expr="lte", label=_("End Date"), field_name="created")

    class Meta:
        model = Order
        fields = [
            "order_form",
            "lineitems__member__user__first_name",
            "lineitems__member__user__last_name",
            "status",
            "start_date",
            "end_date",
        ]

    def filter_queryset(self, queryset) -> QuerySet:
        return super().filter_queryset(queryset).distinct()
