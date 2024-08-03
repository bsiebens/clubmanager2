from .models import Member
from django.views.generic.list import ListView


class MemberListView(ListView):
    model = Member
