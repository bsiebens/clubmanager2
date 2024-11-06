#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

from django.utils import timezone
from rest_framework import serializers

from teams.serializers import TeamNameSerializer as TeamSerializer
from .models import Game, GameType, Opponent


class OpponentSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Opponent
        fields = ["name", "logo"]

    def get_logo(self, obj: Opponent) -> dict[str, str | int]:
        return {"url": obj.logo.url, "width": obj.logo.width, "height": obj.logo.height}


class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ["name", "opponent_count"]


class GameSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    opponent = OpponentSerializer()
    game_type = serializers.SerializerMethodField()
    passed = serializers.SerializerMethodField()
    is_home_game = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["id", "team", "opponent", "date", "location", "live", "score_team", "score_opponent", "game_type", "passed", "is_home_game"]

    def get_game_type(self, obj: Game) -> str:
        return obj.game_type.name

    def get_passed(self, obj: Game) -> bool:
        return obj.date <= timezone.now()

    def get_is_home_game(self, obj: Game) -> bool:
        return obj.is_home_game


class GameSerializerV2(serializers.ModelSerializer):
    team = TeamSerializer()
    opponent = OpponentSerializer()
    game_type = GameTypeSerializer()
    is_passed = serializers.SerializerMethodField()
    is_home_game = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["id", "team", "opponent", "date", "location", "live", "score_team", "score_opponent", "game_type", "is_passed", "is_home_game"]

    def get_is_passed(self, obj: Game) -> bool:
        if obj.date is None:
            return False

        if timezone.is_aware(obj.date):
            return obj.date <= timezone.now()
        else:
            local_timezone = timezone.get_current_timezone()
            obj_date_aware = local_timezone.localize(obj.date)
            return obj_date_aware <= timezone.now()

    def get_is_home_game(self, obj: Game) -> bool:
        return obj.is_home_game
