from rest_framework import viewsets

from .models import Team
from .serializers import TeamSerializer


class TeamsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    lookup_field = "slug"
    serializer_class = TeamSerializer
