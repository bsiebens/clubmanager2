from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView

from teams.models import Season

from .filters import GameFilter
from .models import Game, Opponent


class OpponentsListView(ListView):
    model = Opponent
    paginate_by = 50


class OpponentsAddView(SuccessMessageMixin, CreateView):
    model = Opponent
    fields = ["name", "logo"]
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OpponentsEditView(SuccessMessageMixin, UpdateView):
    model = Opponent
    fields = ["name", "logo"]
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> updated succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OpponentsDeleteView(SuccessMessageMixin, DeleteView):
    model = Opponent
    success_url = reverse_lazy("clubmanager_admin:activities:opponents_index")
    success_message = _("Opponent <strong>%(name)s</strong> deleted succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class GamesListView(FilterView):
    filterset_class = GameFilter
    paginate_by = 50

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


class GamesAddView(SuccessMessageMixin, CreateView):
    model = Game
    fields = ["team", "opponent", "date", "location"]
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M"))


class GamesEditView(SuccessMessageMixin, UpdateView):
    model = Game
    fields = ["team", "opponent", "date", "location"]
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> updated succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M"))


class GamesDeleteView(SuccessMessageMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("clubmanager_admin:activities:games_index")
    success_message = _("Game <strong>%(team)s</strong> versus <strong>%(opponent)s</strong> <strong>(%(date)s)</strong> deleted succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, team=self.object.team, opponent=self.object.opponent, date=self.object.date.strftime("%d %b %Y %H:%M"))
