from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rules.contrib.views import PermissionRequiredMixin
from django.contrib import messages

from .models import Sponsor


class SponsorListView(PermissionRequiredMixin, ListView):
    model = Sponsor
    paginate_by = 25
    permission_required = "frontend"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class SponsorAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Sponsor
    fields = ["name", "url", "logo", "start_date", "end_date"]
    success_url = reverse_lazy("clubmanager_admin:frontend:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> added succesfully")
    permission_required = "frontend"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_initial(self) -> dict[str, Any]:
        initial_data = super(SponsorAddView, self).get_initial()

        initial_data["start_date"] = timezone.now().date()

        return initial_data


class SponsorEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Sponsor
    fields = ["name", "url", "logo", "start_date", "end_date"]
    success_url = reverse_lazy("clubmanager_admin:frontend:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> updated succesfully")
    permission_required = "frontend"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class SponsorDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Sponsor
    success_url = reverse_lazy("clubmanager_admin:frontend:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> deleted succesfully")
    permission_required = "frontend"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)
