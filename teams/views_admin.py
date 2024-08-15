from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from rules.contrib.views import permission_required

from .models import Team


class TeamsListView(ListView):
    model = Team
