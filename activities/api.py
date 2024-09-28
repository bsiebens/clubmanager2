from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets

from .models import Game
from .serializers import GameSerializer
from teams.models import Season
from datetime import timedelta


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = Game.objects.all()
        team = self.request.query_params.get("team", "all")
        count = self.request.query_params.get("count", 5)
        home_games_only = self.request.query_params.get("home_games_only", False)
        all_games_for_season = self.request.query_params.get("all_games_for_season", False)

        queryset = queryset.filter(season=Season.get_season())

        if not all_games_for_season:
            queryset = queryset.filter(Q(date__gte=timezone.now()) | Q(live=True) | Q(date__gte=timezone.now() - timedelta(hours=3)))

        if team != "all":
            queryset = queryset.filter(team__slug=team)

        if home_games_only:
            queryset = queryset.filter(Q(location__iexact="ice skating center mechelen") | Q(location__iexact="iscm"))

        if all_games_for_season:
            return queryset

        return queryset[:count]
