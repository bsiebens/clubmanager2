from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from members.models import Member


class EditorAddForm(forms.Form):
    member = forms.ModelChoiceField(
        queryset=Member.objects.filter(user__is_active=True)
        .exclude(user__groups=Group.objects.get(name="editors"))
        .order_by("user__last_name", "user__first_name"),
        label=_("Member"),
    )

    def save_member(self):
        editors = Group.objects.get(name="editors")
        member = self.cleaned_data["member"]

        member.user.groups.add(editors)

        return self.cleaned_data["member"]
