from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from .models import Member
from django.utils.translation import gettext_lazy as _


class MemberForm(forms.ModelForm):
    first_name = forms.CharField(max_length=250, label=_("First Name"))
    last_name = forms.CharField(max_length=250, label=_("Last Name"))
    email = forms.EmailField(label=_("Email"))

    password = forms.CharField(max_length=250, label=_("Password"), widget=forms.PasswordInput, required=False)
    password_confirmation = forms.CharField(max_length=250, label=_("Password Confirmation"), widget=forms.PasswordInput, required=False)

    class Meta:
        model = Member
        fields = ["phone", "emergency_phone_primary", "emergency_phone_secondary", "is_organization_admin", "license", "birthday"]
        localized_fields = fields

    def save(self, commit: bool = ...) -> Any:
        password = self.cleaned_data["password"] and self.cleaned_data["password"] == self.cleaned_data["password_confirmation"]

        member = Member.create_member(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            username=self.cleaned_data["email"],
            password=password,
            commit=commit,
        )

        return member
