from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from rules.contrib.views import PermissionRequiredMixin
from django.contrib import messages

from .filters import TeamFilter, TeamMembershipFilter, TeamRoleFilter
from .forms import NumberPoolForm, SeasonAddForm, TeamPictureFormSet
from .models import NumberPool, Season, Team, TeamMembership, TeamRole


class TeamsListView(PermissionRequiredMixin, FilterView):
    filterset_class = TeamFilter
    paginate_by = 50
    permission_required = "teams.view_team"
    permission_denied_message = _("You do not have sufficient access rights to access the team list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class TeamsAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Team
    fields = ["name", "short_name", "type", "number_pool", "slug", "logo"]
    success_url = reverse_lazy("clubmanager_admin:teams:teams_index")
    success_message = _("Team <strong>%(name)s</strong> created succesfully")
    permission_required = "teams.add_team"
    permission_denied_message = _("You do not have sufficient access rights to access the team list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

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


class TeamsEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Team
    fields = ["name", "short_name", "type", "number_pool", "slug", "logo"]
    success_url = reverse_lazy("clubmanager_admin:teams:teams_index")
    success_message = _("Team <strong>%(name)s</strong> updated succesfully")
    permission_required = "teams.change_team"
    permission_denied_message = _("You do not have sufficient access rights to access the team list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

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


class TeamsDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Team
    success_url = reverse_lazy("clubmanager_admin:teams:teams_index")
    success_message = _("Team <strong>%(name)s</strong> deleted succesfully")
    permission_required = "teams.delete_team"
    permission_denied_message = _("You do not have sufficient access rights to access the team list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class SeasonListView(PermissionRequiredMixin, ListView):
    model = Season
    permission_required = "teams.view_season"
    permission_denied_message = _("You do not have sufficient access rights to access the season list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(SeasonListView, self).get_context_data(**kwargs)
        context["form"] = SeasonAddForm()

        return context


class SeasonAddView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    form_class = SeasonAddForm
    success_url = reverse_lazy("clubmanager_admin:teams:seasons_index")
    success_message = _("Season added succesfully")
    template_name = "teams/season_form.html"
    permission_required = "teams.ad_season"
    permission_denied_message = _("You do not have sufficient access rights to access the season list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def form_valid(self, form: SeasonAddForm) -> HttpResponse:
        form.save_season()

        return super(SeasonAddView, self).form_valid(form)


class SeasonDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("clubmanager_admin:teams:seasons_index")
    success_message = _("Season deleted succesfully")
    model = Season
    permission_required = "teams.delete_season"
    permission_denied_message = _("You do not have sufficient access rights to access the season list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class NumberPoolListView(PermissionRequiredMixin, ListView):
    model = NumberPool
    permission_required = "teams.view_numberpool"
    permission_denied_message = _("You do not have sufficient access rights to access the numberpool list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NumberPoolListView, self).get_context_data(**kwargs)
        context["form"] = NumberPoolForm

        return context


class NumberPoolAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = NumberPool
    form_class = NumberPoolForm
    success_url = reverse_lazy("clubmanager_admin:teams:numberpools_index")
    success_message = _("Number pool <strong>%(name)s</strong> created succesfully")
    permission_required = "teams.add_numberpool"
    permission_denied_message = _("You do not have sufficient access rights to access the numberpool list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class NumberPoolDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("clubmanager_admin:teams:numberpools_index")
    success_message = _("Number pool <strong>%(name)s</strong> deleted succesfully")
    model = NumberPool
    permission_required = "teams.delete_numberpool"
    permission_denied_message = _("You do not have sufficient access rights to access the numberpool list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class TeamRoleListView(PermissionRequiredMixin, FilterView):
    filterset_class = TeamRoleFilter
    permission_required = "teams.view_teamrole"
    permission_denied_message = _("You do not have sufficient access rights to access the team role list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class TeamRoleAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeamRole
    fields = ["name", "abbreviation", "staff_role", "admin_role", "sort_order"]
    success_url = reverse_lazy("clubmanager_admin:teams:teamroles_index")
    success_message = _("Team role <strong>%(name)s</strong> created succesfully")
    permission_required = "teams.add_teamrole"
    permission_denied_message = _("You do not have sufficient access rights to access the team role list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(TeamRoleAddView, self).get_context_data(**kwargs)

        context["alternate_staff_help_text"] = _("Staff role, displays member on staff section of team pages")
        context["alternate_admin_help_text"] = _("Admin role, can maintain and manage the team")

        return context

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class TeamRoleEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TeamRole
    fields = ["name", "abbreviation", "staff_role", "admin_role", "sort_order"]
    success_url = reverse_lazy("clubmanager_admin:teams:teamroles_index")
    success_message = _("Team role <strong>%(name)s</strong> updated succesfully")
    permission_required = "teams.change_teamrole"
    permission_denied_message = _("You do not have sufficient access rights to access the team role list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(TeamRoleEditView, self).get_context_data(**kwargs)

        context["alternate_staff_help_text"] = _("Staff role, displays member on staff section of team pages")
        context["alternate_admin_help_text"] = _("Admin role, can maintain and manage the team")

        return context

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class TeamRoleDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TeamRole
    success_url = reverse_lazy("clubmanager_admin:teams:teamroles_index")
    success_message = _("Team role <strong>%(name)s</strong> deleted succesfully")
    permission_required = "teams.delete_teamrole"
    permission_denied_message = _("You do not have sufficient access rights to access the team role list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class TeamMembersListView(PermissionRequiredMixin, FilterView):
    filterset_class = TeamMembershipFilter
    paginate_by = 50
    permission_required = "teams.view_teammembership"
    permission_denied_message = _("You do not have sufficient access rights to access the team membership list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_filterset_kwargs(self, filterset_class) -> dict[str, Any]:
        kwargs = super(TeamMembersListView, self).get_filterset_kwargs(filterset_class)

        if kwargs["data"] is None:
            filter_values = {}
        else:
            filter_values = kwargs["data"].dict()

        if not filter_values:
            filter_values.update({"season": str(Season.get_season_id())})

        kwargs["data"] = filter_values

        return kwargs


class TeamMembersAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeamMembership
    success_url = reverse_lazy("clubmanager_admin:teams:teammembers_index")
    success_message = _("Team membership <strong>%(name)s - %(team)s %(season)s</strong> created succesfully")
    fields = ["team", "member", "season", "role", "number", "captain", "assistant_captain"]
    permission_required = "teams.add_teammembership"
    permission_denied_message = _("You do not have sufficient access rights to access the team membership list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.member.get_full_name(), team=self.object.team, season=self.object.season)

    def get_initial(self) -> dict[str, Any]:
        initial = super(TeamMembersAddView, self).get_initial()
        initial["season"] = Season.get_season()

        return initial

    def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
        form = super(TeamMembersAddView, self).get_form(form_class)

        if not self.request.user.member.is_organization_admin:
            form.fields["team"].queryset = Team.objects.filter(teammembership__member__user=self.request.user, teammembership__role__admin_role=True)

        return form


class TeamMembersEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TeamMembership
    success_url = reverse_lazy("clubmanager_admin:teams:teammembers_index")
    success_message = _("Team membership <strong>%(name)s - %(team)s %(season)s</strong> updated succesfully")
    fields = ["team", "member", "season", "role", "number", "captain", "assistant_captain"]
    permission_required = "teams.change_teammembership"
    permission_denied_message = _("You do not have sufficient access rights to access the team membership list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.member.get_full_name(), team=self.object.team, season=self.object.season)

    def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
        form = super(TeamMembersEditView, self).get_form(form_class)

        if not self.request.user.member.is_organization_admin:
            form.fields["team"].queryset = Team.objects.filter(teammembership__member__user=self.request.user, teammembership__role__admin_role=True)

        return form


class TeamMembersDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TeamMembership
    success_url = reverse_lazy("clubmanager_admin:teams:teammembers_index")
    success_message = _("Team memberships <strong>%(name)s - %(team)s %(season)s</strong> deleted succesfully")
    permission_required = "teams.delete_teammembership"
    permission_denied_message = _("You do not have sufficient access rights to access the team membership list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.member.get_full_name(), team=self.object.team, season=self.object.season)


class TeamMembersPreviewView(PermissionRequiredMixin, DetailView):
    model = TeamMembership
    permission_required = "teams.view_teammembership"
    permission_denied_message = _("You do not have sufficient access rights to access the team membership list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
