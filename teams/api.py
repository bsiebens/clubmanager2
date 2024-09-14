from .serializers import TeamMembershipSerializer
from rest_framework import viewsets
from .models import TeamMembership


class TeamMembersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer
