import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Team, TeamMembership, TeamRole


class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = ["type", "name"]


class TeamRoleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Name"))

    class Meta:
        model = TeamRole
        fields = ["name"]


class TeamMembershipFilter(django_filters.FilterSet):
    member__user__first_name = django_filters.CharFilter(lookup_expr="icontains", label=_("First Name"))
    member__user__last_name = django_filters.CharFilter(lookup_expr="icontains", label=_("Last Name"))

    class Meta:
        model = TeamMembership
        fields = ["team", "season", "role", "member__user__first_name", "member__user__last_name"]
