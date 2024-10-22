from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rules.contrib.views import PermissionRequiredMixin

from .models import Order, LineItem, Material, Sponsor


class SponsorListView(PermissionRequiredMixin, ListView):
    model = Sponsor
    paginate_by = 50
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class SponsorAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Sponsor
    fields = ["name", "url", "logo", "start_date", "end_date"]
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> added succesfully")
    permission_required = "finance"
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
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> updated succesfully")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class SponsorDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Sponsor
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> deleted succesfully")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class MaterialListView(PermissionRequiredMixin, ListView):
    model = Material
    paginate_by = 50
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the cost item list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class MaterialAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    fields = ["description", "price", "price_type", "team", "role"]
    success_url = reverse_lazy("clubmanager_admin:finance:materials_index")
    success_message = _("Cost item <strong>%(name)s</strong> added succesfully")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the cost item list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.description)


class MaterialEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    fields = ["description", "price", "price_type", "team", "role"]
    success_url = reverse_lazy("clubmanager_admin:finance:materials_index")
    success_message = _("Cost item <strong>%(name)s</strong> updated succesfully")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the cost item list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.description)


class MaterialDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Material
    success_url = reverse_lazy("clubmanager_admin:finance:materials_index")
    success_message = _("Cost item <strong>%(name)s</strong> deleted succesfully")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the cost item list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.description)
