from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from clubmanager.views import MessagesDeniedMixin
from finance.models import Sponsor


class SponsorListView(MessagesDeniedMixin, ListView):
    model = Sponsor
    paginate_by = 25
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")


class SponsorAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView):
    model = Sponsor
    fields = ["name", "url", "logo"]
    success_message = _("Sponsor <strong>%(name)s</strong> added successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_initial(self) -> dict:
        initial_data = super().get_initial()
        initial_data["start_date"] = timezone.now().date()

        return initial_data


class SponsorEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView):
    model = Sponsor
    fields = ["name", "url", "logo"]
    success_message = _("Sponsor <strong>%(name)s</strong> updated successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class SponsorDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView):
    model = Sponsor
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> deleted successfully")
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)
