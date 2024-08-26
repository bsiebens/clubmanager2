from typing import Any
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView

from .filters import MemberFilter, FamilyFilter
from .forms import MemberForm
from .models import Member, Family


class MemberListView(FilterView):
    filterset_class = MemberFilter
    paginate_by = 50


class MemberDeleteView(SuccessMessageMixin, DeleteView):
    model = Member
    success_url = reverse_lazy("clubmanager_admin:members:members_index")
    success_message = _("Member deleted succesfully")


class MemberAddView(SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("clubmanager_admin:members:members_index")
    success_message = _("Member %(name)s was created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())


class MemberEditView(SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("clubmanager_admin:members:members_index")
    success_message = _("Member %(name)s was updated succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())

    def get_initial(self) -> dict[str, Any]:
        initial_data = super(MemberEditView, self).get_initial()

        initial_data["first_name"] = self.object.first_name
        initial_data["last_name"] = self.object.last_name
        initial_data["email"] = self.object.email

        return initial_data


class FamilyListView(FilterView):
    filterset_class = FamilyFilter
    paginate_by = 50


class FamilyAddView(SuccessMessageMixin, CreateView):
    model = Family
    fields = ["members"]
    localized_fields = fields
    success_url = reverse_lazy("clubmanager_admin:members:families_index")
    success_message = _("Family was created succesfully")


class FamilyEditView(SuccessMessageMixin, UpdateView):
    model = Family
    fields = ["members"]
    localized_fields = fields
    success_url = reverse_lazy("clubmanager_admin:members:families_index")
    success_message = _("Family was updated succesfully")


class FamilyDeleteView(SuccessMessageMixin, DeleteView):
    model = Family
    success_url = reverse_lazy("clubmanager_admin:members:families_index")
    success_message = _("Family deleted succesfully")
