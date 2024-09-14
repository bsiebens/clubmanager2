from .models import Team, TeamMembership, TeamRole
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
