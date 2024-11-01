#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

import importlib

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel

from members.rules import is_organization_admin
from news.rules import is_admin
from teams.models import Season, Team
from .rules import is_team_admin


class GameManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(GameManager, self).get_queryset().select_related("team", "opponent", "season", "game_type")


class Opponent(RulesModel):
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
        rules_permissions = {
            "add": is_admin,
            "view": is_admin,
            "change": is_admin,
            "delete": is_organization_admin,
        }


class GameType(RulesModel):
    name = models.CharField(_("name"), max_length=250)
    opponent_count = models.IntegerField(_("opponent count"), default=1, help_text=_(
        "Number of opponents for this game type, does not have any influence on the working of clubmanager but is passed along in the API."))

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("game type")
        verbose_name_plural = _("game types")
        ordering = ["name"]
        rules_permissions = {
            "add": is_organization_admin,
            "view": is_organization_admin,
            "change": is_organization_admin,
            "delete": is_organization_admin,
        }


class Game(RulesModel):
    COMPETITIONS = {
        "RBIHF": "activities.competition.hockey",
        "CEHL": "activities.competition.hockey",
    }
    COMPETITION_CHOICES = {i: i for i in COMPETITIONS.keys()}

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("team"), related_name="games")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_("season"), related_name="games", default=Season.get_season_id,
                               blank=True, null=True)
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE, verbose_name=_("opponent"), related_name="games", blank=True, null=True)
    date = models.DateTimeField()
    location = models.CharField(_("location"), max_length=250)
    game_type = models.ForeignKey(GameType, on_delete=models.PROTECT, verbose_name=_("game type"), related_name="games")

    competition = models.CharField(_("competition"), max_length=20, choices=COMPETITION_CHOICES, blank=True, null=True)
    game_id = models.CharField(_("game ID"), max_length=250, blank=True, null=True)
    live = models.BooleanField(_("live"), default=False)
    score_team = models.IntegerField(_("score team"), default=0, blank=True, null=True)
    score_opponent = models.IntegerField(_("score opponent"), default=0, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = GameManager()

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
        return self.location.lower() == settings.CLUB_DEFAULT_HOME_LOCATION.lower()

    def update_game_information(self) -> None:
        """Checks if this games belongs to a given competition. If yes, will try to import the competition module and run its update_game_information() function."""

        if self.competition is not None:
            try:
                module_name = self.COMPETITIONS.get(self.competition)

                if module_name is not None:
                    module = importlib.import_module(module_name)
                    competition_class = getattr(module, self.competition)

                    if competition_class is not None:
                        competition_instance = competition_class()
                        competition_instance.update_game_information(game=self)
                    else:
                        print(f"Competition class '{self.competition}' not found in module '{module_name}'")
                else:
                    print(f"Competition '{self.competition}' not found in COMPETITIONS")

            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Error importing module or accessing competition class: {e}")
