from .models import Opponent, Game, GameType
from teams.serializers import TeamNameSerializer
from rest_framework import serializers


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

    class Meta:
        model = Game
        fields = ["id", "team", "opponent", "date", "location", "live", "score_team", "score_opponent", "game_type"]

    def get_game_type(self, obj: Game) -> str:
        return obj.game_type.name
