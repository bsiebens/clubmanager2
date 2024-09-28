from django.utils import timezone
from rest_framework import serializers

from teams.serializers import TeamNameSerializer

from .models import Game, Opponent


class OpponentNameSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Opponent
        fields = ["name", "logo"]

    def get_logo(self, obj: Opponent) -> dict[str, str | int]:
        return {"url": obj.logo.url, "width": obj.logo.width, "height": obj.logo.height}


class GameSerializer(serializers.ModelSerializer):
    team = TeamNameSerializer()
    opponent = OpponentNameSerializer()
    game_type = serializers.SerializerMethodField()
    passed = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["id", "team", "opponent", "date", "location", "live", "score_team", "score_opponent", "game_type", "passed"]

    def get_game_type(self, obj: Game) -> str:
        return obj.game_type.name

    def get_passed(self, obj: Game) -> bool:
        return obj.date <= timezone.now()
