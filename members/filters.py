import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Member


class MemberFilter(django_filters.FilterSet):
    user__first_name = django_filters.CharFilter(lookup_expr="icontains", label=_("First Name"))
    user__last_name = django_filters.CharFilter(lookup_expr="icontains", label=_("Last Name"))

    class Meta:
        model = Member
        fields = ["user__first_name", "user__last_name"]
