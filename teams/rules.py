import rules
from django.contrib.auth.models import AbstractUser

from news.rules import is_admin


@rules.predicate
def is_team_admin(user: AbstractUser | None, teammembership) -> bool:
    from .models import Season, TeamMembership

    season = Season.get_season()

    if user is not None:
        if teammembership is not None:
            return TeamMembership.objects.filter(member__user=user, team=teammembership.team, season=season, role__admin_role=True).exists()

        return TeamMembership.objects.filter(member__user=user, season=season, role__admin_role=True).exists()

    return False


rules.add_perm("teams", is_admin)
