from itertools import chain

from django.db.models import Q
from rest_framework import serializers

from .models import Season, Team, TeamMembership, TeamPicture, TeamRole


class TeamNameSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["name", "logo"]

    def get_logo(self, obj: Team) -> dict[str, str | int]:
        return {"url": obj.logo.url, "width": obj.logo.width, "height": obj.logo.height}


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
    goalie = serializers.SerializerMethodField()
    forward = serializers.SerializerMethodField()
    defense = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["slug", "name", "short_name", "picture", "goalie", "forward", "defense", "staff"]
        lookup_field = "slug"

    def get_picture(self, obj: Team) -> str:
        try:
            picture = obj.teampicture_set.get(season=Season.get_season()).picture
            return {"url": picture.url, "width": picture.width, "height": picture.height}

        except TeamPicture.DoesNotExist:
            return {"url": "", "height": 0, "width": 0}

    def get_goalie(self, obj: Team) -> list[TeamMembership]:
        return TeamMembershipSerializer(obj.teammembership_set.filter(season=Season.get_season()).filter(role__abbreviation="GO").order_by("number"), many=True).data

    def get_forward(self, obj: Team) -> list[TeamMembership]:
        return TeamMembershipSerializer(obj.teammembership_set.filter(season=Season.get_season()).filter(role__abbreviation="F").order_by("number"), many=True).data

    def get_defense(self, obj: Team) -> list[TeamMembership]:
        return TeamMembershipSerializer(obj.teammembership_set.filter(season=Season.get_season()).filter(role__abbreviation="D").order_by("number"), many=True).data

    def get_staff(self, obj: Team) -> list[TeamMembership]:
        head_coach = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="CO").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        assistant_coach = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="AC").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        general_manager = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="GM").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        team_manager = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="TM").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        others = (
            obj.teammembership_set.filter(season=Season.get_season(), number=None)
            .exclude(
                Q(role__abbreviation="GO")
                | Q(role__abbreviation="F")
                | Q(role__abbreviation="D")
                | Q(role__abbreviation="CO")
                | Q(role__abbreviation="AC")
                | Q(role__abbreviation="GM")
                | Q(role__abbreviation="TM")
            )
            .order_by("member__user__last_name", "member__user__first_name", "member__license")
        )

        return TeamMembershipSerializer(list(chain(head_coach, assistant_coach, general_manager, team_manager, others)), many=True).data
