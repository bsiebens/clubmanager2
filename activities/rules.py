import rules
from django.contrib.auth.models import AbstractUser

from news.rules import is_admin


@rules.predicate
def is_team_admin(user: AbstractUser | None, game) -> bool:
    from teams.models import Season, TeamMembership

    season = Season.get_season()

    if user is not None:
        if game is not None:
            return TeamMembership.objects.filter(member__user=user, team=game.team, season=season, role__admin_role=True).exists()

        return TeamMembership.objects.filter(member__user=user, season=season, role__admin_role=True).exists()

    return False


rules.add_perm("activities", is_admin)
