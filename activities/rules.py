#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

import rules
from django.contrib.auth.models import AbstractUser

from news.rules import is_admin


@rules.predicate
def is_team_admin(user: AbstractUser | None, game: "Game | None") -> bool:
    """Returns True if user is set and user has a team role that is flagged as admin for a team linked to the given game. Otherwise, returns False."""

    from teams.models import Season, TeamMembership

    if user is not None:
        if game is not None:
            return TeamMembership.objects.filter(member__user=user, team=game.team, season=game.season, role__admin_role=True).exists()
        else:
            return TeamMembership.objects.filter(member__user=user, role__admin_role=True, season=Season.get_season_id()).exists()

    return False


rules.add_perm("activities", is_admin)
