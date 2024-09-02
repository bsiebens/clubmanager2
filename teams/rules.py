import rules
from django.contrib.auth.models import AbstractUser

from .models import Team, TeamRole, TeamMembership, Season


@rules.predicate
def is_team_admin(user: AbstractUser | None, team: Team | None) -> bool:
    season = Season.get_season()

    if team is not None:
        memberships = TeamMembership.objects.filter(member__user=user, team=team, season=season)

        for membership in memberships:
            if membership.role.admin_role:
                return True

        return False
