from typing import Any
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from members.models import Member
from .models import NewsItem


class EditorAddForm(forms.Form):
    member = forms.ModelChoiceField(
        queryset=Member.objects.filter(user__is_active=True).exclude(user__groups__name="editors").order_by("user__last_name", "user__first_name"),
        label=_("Member"),
    )

    def save_member(self):
        editors = Group.objects.get(name="editors")
        member = self.cleaned_data["member"]

        member.user.groups.add(editors)

        return self.cleaned_data["member"]


class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ["title", "text", "type", "publish_on"]
        localized_fields = fields
