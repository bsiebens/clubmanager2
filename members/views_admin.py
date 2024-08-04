from typing import Any
from django.db.models.query import QuerySet
from .models import Member
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import render
from .filters import MemberFilter
from django_filters.views import FilterView


class MemberList(FilterView):
    filterset_class = MemberFilter
    paginate_by = 50
