# from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from members.models import Member

from .models import Season, Team, TeamMembership


# @shared_task
def update_group_membership(user_id: int) -> None:
    user = get_user_model().objects.get(pk=user_id)
    member = Member.objects.get(user=user)
    season = Season.get_season()

    teams = Team.objects.filter(teammembership__member=member, teammembership__season=season)
    admin_memberships = TeamMembership.objects.filter(member=member, season=season, role__admin_role=True).count()
    groups = [team.slug for team in teams.distinct()]

    if (admin_memberships > 0 or member.is_organization_admin) and "admin" not in groups:
        groups.append("admin")

    if admin_memberships == 0 and not member.is_organization_admin:
        while "admin" in groups:
            groups.remove("admin")

    if member.user.groups.filter(name="editors").exists():
        groups.append("editors")

    groups = Group.objects.filter(name__in=groups)
    user.groups.set(groups)
