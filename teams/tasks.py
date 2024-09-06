from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from members.models import Member

from .models import Season, Team


# @shared_task
def update_group_membership(user_id: int) -> None:
    user = get_user_model().objects.get(pk=user_id)
    member = Member.objects.get(user=user)
    season = Season.get_season()

    memberships = Team.objects.filter(teammembership__member__user=user, teammembership__season=season)
    admin_memberships = memberships.filter(teammembership__role__admin_role=True).count()

    groups = [team.slug for team in memberships.distinct()]
    if admin_memberships > 0 or member.is_organization_admin:
        groups.append("admin")

    if member.user.groups.get(name="editors").exists():
        groups.append("editors")

    groups = Group.objects.filter(name__in=groups)
    user.groups.set(groups)
