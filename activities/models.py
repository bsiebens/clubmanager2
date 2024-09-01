from typing import Iterable
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from teams.models import Team, Season


class Opponent(models.Model):
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


class Game(models.Model):
    """A game"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("team"), related_name="games")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_("season"), related_name="games", default=Season.get_season_id, blank=True, null=True)
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE, verbose_name=_("opponent"), related_name="games")
    date = models.DateTimeField()
    location = models.CharField(_("location"), max_length=250, default="Ice Skating Center Mechelen")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{i.team} vs {i.opponent}".format(i=self)

    class Meta:
        verbose_name = _("game")
        verbose_name_plural = _("games")
        ordering = ["date"]

    def save(self, *args, **kwargs) -> None:
        self.season = Season.get_season(date=self.date.date())

        return super(Game, self).save(*args, **kwargs)

    @property
    @admin.display(description=_("Home game?"), boolean=True)
    def is_home_game(self) -> bool:
        return self.location.lower() == "ice skating center mechelen" or self.location.lower() == "iscm"
