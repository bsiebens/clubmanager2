import csv
import io
from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django_filters.views import FilterView
from rules.contrib.views import PermissionRequiredMixin

from .filters import FamilyFilter, MemberFilter
from .forms import MassUploadForm, MemberForm
from .models import Family, Member


class MemberListView(PermissionRequiredMixin, FilterView):
    filterset_class = MemberFilter
    paginate_by = 50
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class MemberDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Member
    success_url = reverse_lazy("clubmanager_admin:members:members_index")
    success_message = _("Member <strong>%(name)s</strong> deleted succesfully")
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())


class MemberAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("clubmanager_admin:members:members_index")
    success_message = _("Member <strong>%(name)s</strong> added succesfully - <strong>%(note)s</strong>")
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name(), note=self.object.notes)


class MemberEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("clubmanager_admin:members:members_index")
    success_message = _("Member <strong>%(name)s</strong> updated succesfully")
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())

    def get_initial(self) -> dict[str, Any]:
        initial_data = super(MemberEditView, self).get_initial()

        initial_data["first_name"] = self.object.first_name
        initial_data["last_name"] = self.object.last_name
        initial_data["email"] = self.object.email

        return initial_data


class FamilyListView(PermissionRequiredMixin, FilterView):
    filterset_class = FamilyFilter
    paginate_by = 50
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class FamilyAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Family
    fields = ["members"]
    localized_fields = fields
    success_url = reverse_lazy("clubmanager_admin:members:families_index")
    success_message = _("Family added succesfully")
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class FamilyEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Family
    fields = ["members"]
    localized_fields = fields
    success_url = reverse_lazy("clubmanager_admin:members:families_index")
    success_message = _("Family updated succesfully")
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class FamilyDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Family
    success_url = reverse_lazy("clubmanager_admin:members:families_index")
    success_message = _("Family deleted succesfully")
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class MassUploadView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    form_class = MassUploadForm
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")
    success_url = reverse_lazy("clubmanager_admin:members:members_index")
    success_message = _("Members have been uploaded succesfully")
    template_name = "members/member_bulk_load.html"

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def form_valid(self, form: MassUploadForm) -> HttpResponse:
        from teams.models import Season, Team, TeamMembership, TeamRole

        member_data = self.request.FILES["member_data"]
        season = Season.get_season()
        roles = {role.abbreviation: role for role in TeamRole.objects.all()}
        teams = {team.short_name: team for team in Team.objects.all()}

        team_memberships = []

        with io.TextIOWrapper(member_data.file) as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                member_information = {
                    "first_name": row[0],
                    "last_name": row[1],
                    "email": row[2],
                    "birthday": row[3],
                    "license": row[4],
                    "team": row[5],
                    "role": row[6],
                    "number": 0 if row[7] == "" else row[7],
                    "captain": True if row[8].upper() == "C" else False,
                    "assistant_captain": True if row[8].upper() == "A" else False,
                }

                member = Member.create_member(
                    first_name=member_information["first_name"],
                    last_name=member_information["last_name"],
                    email=member_information["email"],
                    username=member_information["email"],
                )
                member.license = member_information["license"]

                if member_information["birthday"] is not None and member_information["birthday"] != "":
                    member.birthday = member_information["birthday"]

                member.save(update_fields=["license", "birthday"])

                if member_information["team"] is not None and member_information["team"] != "":
                    team_memberships.append(
                        TeamMembership(
                            team=teams[member_information["team"]],
                            role=roles[member_information["role"]],
                            season=season,
                            member=member,
                            number=member_information["number"],
                            captain=member_information["captain"],
                            assistant_captain=member_information["assistant_captain"],
                        )
                    )

        TeamMembership.objects.bulk_create(team_memberships)

        return super(MassUploadView, self).form_valid(form)
