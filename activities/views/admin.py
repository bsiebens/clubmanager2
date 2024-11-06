#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from rules.contrib.views import permission_required

from clubmanager.views import MessagesDeniedMixin
from teams.models import Season, Team
from ..filters import GameFilter
from ..models import Game, GameType, Opponent


class GameTypeListView(MessagesDeniedMixin, ListView):
    model = GameType
    permission_required = "activities.view_gametype"
    permission_denied_message = _("You do not have sufficient access rights to access the game type list")


class GameTypeAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView):
    model = GameType
    fields = ["name", "opponent_count"]
    success_url = reverse_lazy("clubmanager_admin:activities:gametypes_index")
    success_message = _("Game type <strong>%(name)s</strong> created succesfully")
    permission_required = "activities.add_gametype"
    permission_denied_message = GameTypeListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class GameTypeEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView):
    model = GameType
    fields = ["name", "opponent_count"]
    success_url = reverse_lazy("clubmanager_admin:activities:gametypes_index")
    success_message = _("Game type <strong>%(name)s</strong> updated succesfully")
    permission_required = "activities.edit_gametype"
    permission_denied_message = GameTypeListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class GameTypeDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView):
    model = GameType
    success_url = reverse_lazy("clubmanager_admin:activities:gametypes_index")
    success_message = _("Game type <strong>%(name)s</strong> deleted succesfully")
    permission_required = "activities.delete_gametype"
    permission_denied_message = GameTypeListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OpponentListView(MessagesDeniedMixin, ListView):
    model = Opponent
    permission_required = "activities.view_opponent"
    permission_denied_message = _("You do not have sufficient access rights to access the opponent list")
    paginate_by = 25


class OpponentAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView):
    model = Opponent
    fields = ["name", "logo"]
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> created succesfully")
    permission_required = "activities.add_opponent"
    permission_denied_message = OpponentListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OpponentEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView):
    model = Opponent
    fields = ["name", "logo"]
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> updated succesfully")
    permission_required = "activities.change_opponent"
    permission_denied_message = OpponentListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OpponentDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView):
    model = Opponent
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> deleted succesfully")
    permission_required = "activities.change_opponent"
    permission_denied_message = OpponentListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class GameListView(MessagesDeniedMixin, FilterView):
    filterset_class = GameFilter
    paginate_by = 25
    permission_required = "activities.view_game"
    permission_denied_message = _("You do not have sufficient access rights to view the game list")

    def get_filterset_kwargs(self, filterset_class: GameFilter) -> dict[str, Any]:
        # Set the default season to the current season if no filter values are set

        filter_values = {"season": str(Season.get_season_id())}
        kwargs = super().get_filterset_kwargs(filterset_class)

        if kwargs["data"] is not None:
            filter_values = kwargs["data"].dict()

        kwargs["data"] = filter_values
        return kwargs


class GameAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView):
    model = Game
    fields = ["team", "opponent", "date", "location", "competition", "game_id", "game_type"]
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> vs. <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> created succesfully")
    permission_required = "activities.add_game"
    permission_denied_message = GameListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(
            cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M")
        )

    def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
        # Sets the default location for the game and restricts the list of teams to those the user is an admin for

        form = super().get_form(form_class)
        form.fields["location"].initial = settings.CLUB_DEFAULT_HOME_LOCATION

        if not self.request.user.member.is_organization_admin:
            form.fields["team"].queryset = Team.objects.filter(teammembership__member__user=self.request.user, teammembership__role__admin_role=True)

        return form


class GameEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView):
    model = Game
    fields = ["team", "opponent", "date", "location", "competition", "game_id", "game_type", "live", "score_team", "score_opponent"]
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> vs. <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> updated succesfully")
    permission_required = "activities.change_game"
    permission_denied_message = GameListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(
            cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M")
        )

    def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
        # Restricts the list of teams to those the user is an admin for

        form = super().get_form(form_class)

        if not self.request.user.member.is_organization_admin:
            form.fields["team"].queryset = Team.objects.filter(teammembership__member__user=self.request.user, teammembership__role__admin_role=True)

        return form


class GameDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> vs. <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> deleted succesfully")
    permission_required = "activities.delete_game"
    permission_denied_message = GameListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(
            cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M")
        )


class GamePreviewView(MessagesDeniedMixin, DetailView):
    model = Game
    permission_required = "activities.view_game"
    permission_denied_message = GameListView.permission_denied_message


@permission_required("activities.edit_game")
def refresh_game_information(request, pk: int) -> HttpResponseRedirect:
    game = Game.objects.get(id=pk)
    game.update_game_information()

    success_message = _("Game <strong>%(team)s</strong> vs. <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> - new information fetched")
    messages.success(request, success_message % dict(team=game.team, opponent=game.opponent, date=game.date.strftime("%d %b %Y %H:%M")))

    return HttpResponseRedirect(reverse_lazy("clubmanager_admin:activities:games_edit", args=[pk]))
