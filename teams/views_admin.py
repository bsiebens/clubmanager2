from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django_filters.views import FilterView
from rules.contrib.views import permission_required

from .models import Season, Team, TeamRole, TeamMembership, TeamPicture, NumberPool
from .forms import SeasonAddForm, NumberPoolForm


class TeamsListView(ListView):
    model = Team


class SeasonListView(ListView):
    model = Season

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(SeasonListView, self).get_context_data(**kwargs)
        context["form"] = SeasonAddForm()

        return context


class SeasonAddView(SuccessMessageMixin, FormView):
    form_class = SeasonAddForm
    success_url = reverse_lazy("clubmanager_admin:teams:seasons_index")
    success_message = _("Season was added succesfully")
    template_name = "teams/season_form.html"

    def form_valid(self, form: SeasonAddForm) -> HttpResponse:
        form.save_season()

        return super(SeasonAddView, self).form_valid(form)


class SeasonDeleteView(SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("clubmanager_admin:teams:seasons_index")
    success_message = _("Season was succesfully removed")
    model = Season


class NumberPoolListView(ListView):
    model = NumberPool

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NumberPoolListView, self).get_context_data(**kwargs)
        context["form"] = NumberPoolForm

        return context


class NumberPoolAddView(SuccessMessageMixin, CreateView):
    model = NumberPool
    form_class = NumberPoolForm
    success_url = reverse_lazy("clubmanager_admin:teams:numberpools_index")
    success_message = _("Number pool %(name)s was created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, title=self.object.name)


class NumberPoolDeleteView(SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("clubmanager_admin:teams:numberpools_index")
    success_message = _("Number pool was succesfully removed")
    model = NumberPool
