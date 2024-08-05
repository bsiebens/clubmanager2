from django_filters.views import FilterView
from django.views.generic.edit import DeleteView

from .filters import MemberFilter
from .models import Member
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


class MemberListView(FilterView):
    filterset_class = MemberFilter
    paginate_by = 50


class MemberDeleteView(SuccessMessageMixin, DeleteView):
    model = Member
    success_url = reverse_lazy("clubmanager_admin:members:index")
    success_message = _("Member was succesfully deleted")
