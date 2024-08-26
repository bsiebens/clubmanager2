from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView

from .filters import TeamFilter, TeamMembershipFilter, TeamRoleFilter
from .forms import NumberPoolForm, SeasonAddForm, TeamPictureFormSet
from .models import NumberPool, Season, Team, TeamMembership, TeamRole


class TeamsListView(FilterView):
    filterset_class = TeamFilter
    paginate_by = 50


class TeamsAddView(SuccessMessageMixin, CreateView):
    model = Team
    fields = ["name", "short_name", "type", "number_pool"]
    success_url = reverse_lazy("clubmanager_admin:teams:teams_index")
    success_message = _("Team %(name)s was created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(TeamsAddView, self).get_context_data(**kwargs)

        if self.request.POST:
            context["pictures"] = TeamPictureFormSet(self.request.POST, self.request.FILES)
        else:
            context["pictures"] = TeamPictureFormSet()

        return context

    def form_valid(self, form) -> HttpResponse:
        context = self.get_context_data()

        pictures = context["pictures"]
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()

            if pictures.is_valid():
                pictures.instance = self.object
                pictures.save()

        return super(TeamsAddView, self).form_valid(form)


class TeamsEditView(SuccessMessageMixin, UpdateView):
    model = Team
    fields = ["name", "short_name", "type", "number_pool"]
    success_url = reverse_lazy("clubmanager_admin:teams:teams_index")
    success_message = _("Team %(name)s was updated succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(TeamsEditView, self).get_context_data(**kwargs)

        if self.request.POST:
            context["pictures"] = TeamPictureFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context["pictures"] = TeamPictureFormSet(instance=self.object)

        return context

    def form_valid(self, form) -> HttpResponse:
        context = self.get_context_data()

        pictures = context["pictures"]
        with transaction.atomic():
            self.object = form.save()

            if pictures.is_valid():
                pictures.save()

        return super(TeamsEditView, self).form_valid(form)


class TeamsDeleteView(SuccessMessageMixin, DeleteView):
    model = Team
    success_url = reverse_lazy("clubmanager_admin:teams:teams_index")
    success_message = _("Team deleted succesfully")


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


class TeamRoleListView(FilterView):
    filterset_class = TeamRoleFilter


class TeamRoleAddView(SuccessMessageMixin, CreateView):
    model = TeamRole
    fields = ["name", "abbreviation", "staff_role", "admin_role", "sort_order"]
    success_url = reverse_lazy("clubmanager_admin:teams:teamroles_index")
    success_message = _("Team role %(name)s was created succesfully")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(TeamRoleAddView, self).get_context_data(**kwargs)

        context["alternate_staff_help_text"] = _("Staff role, displays member on staff section of team pages")
        context["alternate_admin_help_text"] = _("Admin role, can maintain and manage the team")

        return context

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class TeamRoleEditView(SuccessMessageMixin, UpdateView):
    model = TeamRole
    fields = ["name", "abbreviation", "staff_role", "admin_role", "sort_order"]
    success_url = reverse_lazy("clubmanager_admin:teams:teamroles_index")
    success_message = _("Team role %(name)s was updated succesfully")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(TeamRoleEditView, self).get_context_data(**kwargs)

        context["alternate_staff_help_text"] = _("Staff role, displays member on staff section of team pages")
        context["alternate_admin_help_text"] = _("Admin role, can maintain and manage the team")

        return context

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class TeamRoleDeleteView(SuccessMessageMixin, DeleteView):
    model = TeamRole
    success_url = reverse_lazy("clubmanager_admin:teams:teamroles_index")
    success_message = _("Team role deleted succesfully")


class TeamMembersListView(FilterView):
    filterset_class = TeamMembershipFilter
    paginate_by = 50

    def get_filterset_kwargs(self, filterset_class) -> dict[str, Any]:
        kwargs = super(TeamMembersListView, self).get_filterset_kwargs(filterset_class)

        if kwargs["data"] is None:
            filter_values = {}
        else:
            filter_values = kwargs["data"].dict()

        if not filter_values:
            filter_values.update({"season": str(Season.get_season().id)})

        kwargs["data"] = filter_values

        return kwargs


class TeamMembersAddView(SuccessMessageMixin, CreateView):
    model = TeamMembership
    success_url = reverse_lazy("clubmanager_admin:teams:teammembers_index")
    success_message = _("Team membership %(name)s - %(team)s %(season)s was created succesfully")
    fields = ["team", "member", "season", "role", "number", "captain", "assistant_captain"]

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.member.get_full_name(), team=self.object.team, season=self.object.season)


class TeamMembersEditView(SuccessMessageMixin, UpdateView):
    model = TeamMembership
    success_url = reverse_lazy("clubmanager_admin:teams:teammembers_index")
    success_message = _("Team membership %(name)s - %(team)s %(season)s was updated succesfully")
    fields = ["team", "member", "season", "role", "number", "captain", "assistant_captain"]

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.member.get_full_name(), team=self.object.team, season=self.object.season)


class TeamMembersDeleteView(SuccessMessageMixin, DeleteView):
    model = TeamMembership
    success_url = reverse_lazy("clubmanager_admin:teams:teammembers_index")
    success_message = _("Team memberships deleted succesfully")
