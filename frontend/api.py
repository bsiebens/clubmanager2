from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets

from .models import Sponsor
from .serializers import SponsorSerializer


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sponsor.objects.filter(start_date__lte=timezone.now()).filter(Q(end_date__gte=timezone.now()) | Q(end_date=None))
    serializer_class = SponsorSerializer
