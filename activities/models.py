import importlib

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel

from members.rules import is_organization_admin
from news.rules import is_admin
from teams.models import Season, Team

from .rules import is_team_admin


class Opponent(RulesModel):
    """A class holding data on opponents"""

    name = models.CharField(_("name"), max_length=250)
    logo = models.ImageField(_("logo"), upload_to="opponent/logo/")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("opponent")
        verbose_name_plural = _("opponents")
        ordering = ["name"]
        rules_permissions = {"add": is_admin, "view": is_admin, "change": is_admin, "delete": is_organization_admin}


class Game(RulesModel):
    """A game"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("team"), related_name="games")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_("season"), related_name="games", default=Season.get_season_id, blank=True, null=True)
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE, verbose_name=_("opponent"), related_name="games")
    date = models.DateTimeField()
    location = models.CharField(_("location"), max_length=250, default="Ice Skating Center Mechelen")

    competition = models.ForeignKey("Competition", on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("competition"))
    game_id = models.CharField(_("game_id"), max_length=250)
    live = models.BooleanField(_("live"), default=False)
    score_team = models.IntegerField(_("score team"), default=0)
    score_opponent = models.IntegerField(_("score opponent"), default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{i.team} vs {i.opponent}".format(i=self)

    class Meta:
        verbose_name = _("game")
        verbose_name_plural = _("games")
        ordering = ["date"]
        rules_permissions = {
            "add": is_team_admin | is_organization_admin,
            "view": is_admin,
            "change": is_team_admin | is_organization_admin,
            "delete": is_team_admin | is_organization_admin,
        }

    def save(self, *args, **kwargs) -> None:
        self.season = Season.get_season(date=self.date.date())

        return super(Game, self).save(*args, **kwargs)

    @property
    @admin.display(description=_("Home game?"), boolean=True)
    def is_home_game(self) -> bool:
        return self.location.lower() == "ice skating center mechelen" or self.location.lower() == "iscm"

    def update_game_information(self):
        module = importlib.import_module(self.competition.module)
        competition = getattr(module, self.competition.name)

        competition().update_game_information(game=self)


class Competition(models.Model):
    """A competition has a name with a specific URL to fetch data from. These are managed centrally."""

    name = models.CharField(max_length=250)
    module = models.CharField(max_length=250)

    def __str__(self):
        return self.name
