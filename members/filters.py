import django_filters

from .models import Member


class MemberFilter(django_filters.FilterSet):
    class Meta:
        model = Member
        fields = {
            "user__first_name": ["icontains"],
            "user__last_name": ["icontains"],
        }
