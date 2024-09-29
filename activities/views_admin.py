from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from rules.contrib.views import PermissionRequiredMixin, permission_required

from teams.models import Season, Team

from .filters import GameFilter
from .models import Game, Opponent, GameType
from .forms import GameTypeForm


class GameTypeListView(PermissionRequiredMixin, ListView):
    model = GameType
    permission_required = "activities.view_gametype"
    permission_denied_message = _("You do not have sufficient access rights to access the game type list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(GameTypeListView, self).get_context_data(**kwargs)
        context["form"] = GameTypeForm

        return context


class GameTypeAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = GameType
    form_class = GameTypeForm
    success_url = reverse_lazy("clubmanager_admin:activities:gametypes_index")
    success_message = _("Game type <strong>%(name)s</strong> created succesfully")
    permission_required = "activities.edit_gametype"
    permission_denied_message = _("You do not have sufficient access rights to access the game type list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class GameTypeDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("clubmanager_admin:activities:gametypes_index")
    success_message = _("Game type <strong>%(name)s</strong> deleted succesfully")
    model = GameType
    permission_required = "activities.delete_gametype"
    permission_denied_message = _("You do not have sufficient access rights to access the game type list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OpponentsListView(PermissionRequiredMixin, ListView):
    model = Opponent
    paginate_by = 25
    permission_required = "activities.view_opponent"
    permission_denied_message = _("You do not have sufficient access rights to access the opponent list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class OpponentsAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Opponent
    fields = ["name", "logo"]
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> created succesfully")
    permission_required = "activities.add_opponent"
    permission_denied_message = _("You do not have sufficient access rights to access the opponent list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OpponentsEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Opponent
    fields = ["name", "logo"]
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> updated succesfully")
    permission_required = "activities.change_opponent"
    permission_denied_message = _("You do not have sufficient access rights to edit opponent <strong>%(name)s</strong>")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_permission_denied_message(self) -> str:
        return self.permission_denied_message % dict(name=self.get_object().name)


class OpponentsDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Opponent
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> deleted succesfully")
    permission_required = "activities.delete_opponent"
    permission_denied_message = _("You do not have sufficient access rights to delete opponent <strong>%(name)s</strong>")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_permission_denied_message(self) -> str:
        return self.permission_denied_message % dict(name=self.get_object().name)


class GamesListView(PermissionRequiredMixin, FilterView):
    filterset_class = GameFilter
    paginate_by = 25
    permission_required = "activities.view_game"
    permission_denied_message = _("You do not have sufficient access rights to access the game list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_filterset_kwargs(self, filterset_class) -> dict[str, Any]:
        kwargs = super(GamesListView, self).get_filterset_kwargs(filterset_class)

        if kwargs["data"] is None:
            filter_values = {}
        else:
            filter_values = kwargs["data"].dict()

        if not filter_values:
            filter_values.update({"season": str(Season.get_season_id())})

        kwargs["data"] = filter_values

        return kwargs


class GamesAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Game
    fields = ["team", "opponent", "date", "location", "competition", "game_id", "game_type"]
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> created succesfully")
    permission_required = "activities.add_game"
    permission_denied_message = _("You do not have sufficient access rights to access the game list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M"))

    def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
        form = super(GamesAddView, self).get_form(form_class)

        if not self.request.user.member.is_organization_admin:
            form.fields["team"].queryset = Team.objects.filter(teammembership__member__user=self.request.user, teammembership__role__admin_role=True)

        return form


class GamesEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Game
    fields = ["team", "opponent", "date", "location", "live", "score_team", "score_opponent", "competition", "game_id", "game_type"]
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> updated succesfully")
    permission_required = "activities.change_game"
    permission_denied_message = _(
        "You do not have sufficient access rights to edit game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong>"
    )

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M"))

    def get_permission_denied_message(self) -> str:
        return self.permission_denied_message % dict(team=self.get_object().team, opponent=self.get_object().opponent, date=self.get_object().date.strftime("%d %b %Y %H:%M"))

    def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
        form = super(GamesEditView, self).get_form(form_class)

        if not self.request.user.member.is_organization_admin:
            form.fields["team"].queryset = Team.objects.filter(teammembership__member__user=self.request.user, teammembership__role__admin_role=True)

        return form


class GamesDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> deleted succesfully")
    permission_required = "activities.delete_game"
    permission_denied_message = _(
        "You do not have sufficient access rights to delete game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong>"
    )

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M"))

    def get_permission_denied_message(self) -> str:
        return self.success_message % dict(team=self.get_object().team, opponent=self.get_object().opponent, date=self.get_object().date.strftime("%d %b %Y %H:%M"))


class GamePreviewView(PermissionRequiredMixin, DetailView):
    model = Game
    permission_required = "activities.view_game"
    permission_denied_message = _("You do not have sufficient access rights to access the game list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


@permission_required("activities.edit_game")
def update_game_information(request, pk: int) -> HttpResponse:
    game = Game.objects.get(pk=pk)
    game.update_game_information()

    messages.success(request, _("Game <strong>%(game)s</strong> refreshed" % ({"game": game})))

    return HttpResponseRedirect(reverse_lazy("clubmanager_admin:activities:games_edit", args=[pk]))
