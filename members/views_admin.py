from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from rules.contrib.views import PermissionRequiredMixin

from .filters import FamilyFilter, MemberFilter
from .forms import MemberForm
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
    success_message = _("Member <strong>%(name)s</strong> added succesfully")
    permission_required = "members"
    permission_denied_message = _("You do not have sufficient access rights to access the member list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())


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
