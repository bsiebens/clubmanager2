from .serializers import TeamMembershipSerializer, TeamSerializer
from rest_framework import viewsets
from .models import TeamMembership, Team


class TeamMembersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer


class TeamsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
