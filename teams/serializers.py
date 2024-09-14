from .models import Season, Team, TeamMembership, TeamPicture, TeamRole
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team


class TeamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRole
        fields = ["name", "abbreviation"]


class TeamMembershipSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="member.user.first_name")
    last_name = serializers.CharField(source="member.user.last_name")
    birth_year = serializers.IntegerField(source="member.birthday.year")
    license_number = serializers.CharField(source="member.license")
    role = TeamRoleSerializer()

    class Meta:
        model = TeamMembership
        fields = ["first_name", "last_name", "birth_year", "license_number", "role", "captain", "assistant_captain", "number"]


class TeamSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    goalie = TeamMembershipSerializer(many=True)

    class Meta:
        model = Team
        fields = ["slug", "name", "short_name", "picture", "goalie"]

    def get_picture(self, obj: Team) -> str:
        try:
            picture = obj.teampicture_set.get(season=Season.get_season()).picture
            return {"url": picture.url, "width": picture.width, "height": picture.height}

        except TeamPicture.DoesNotExist:
            return {"url": "", "height": 0, "width": 0}

    def get_goalie(self, obj: Team) -> list[TeamMembership]:
        return obj.teammembership_set.filter(season=Season.get_season()).filter(role__abbreviation="GO").order_by("number")
