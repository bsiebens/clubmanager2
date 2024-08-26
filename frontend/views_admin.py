from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Sponsor


class SponsorListView(ListView):
    model = Sponsor
    paginate_by = 50


class SponsorAddView(SuccessMessageMixin, CreateView):
    model = Sponsor
    fields = ["name", "url", "logo", "start_date", "end_date"]
    success_url = reverse_lazy("clubmanager_admin:frontend:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> added succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_initial(self) -> dict[str, Any]:
        initial_data = super(SponsorAddView, self).get_initial()

        initial_data["start_date"] = timezone.now().date()

        return initial_data


class SponsorEditView(SuccessMessageMixin, UpdateView):
    model = Sponsor
    fields = ["name", "url", "logo", "start_date", "end_date"]
    success_url = reverse_lazy("clubmanager_admin:frontend:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> updated succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class SponsorDeleteView(SuccessMessageMixin, DeleteView):
    model = Sponsor
    success_url = reverse_lazy("clubmanager_admin:frontend:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> deleted succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)
