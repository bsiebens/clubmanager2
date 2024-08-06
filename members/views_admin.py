from typing import Any
from django.forms import BaseForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from django_filters.views import FilterView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from .filters import MemberFilter
from .models import Member
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from .forms import MemberForm


class MemberListView(FilterView):
    filterset_class = MemberFilter
    paginate_by = 50


class MemberDeleteView(SuccessMessageMixin, DeleteView):
    model = Member
    success_url = reverse_lazy("clubmanager_admin:members:index")
    success_message = _("Member was succesfully deleted")


class MemberAddView(SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("clubmanager_admin:members:index")
    success_message = _("Member %(name)s was created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())
