from django import forms
from django.utils.translation import gettext_lazy as _
import csv
from .models import Member


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

    def save(self, commit: bool = True) -> Member:
        password = None

        if self.cleaned_data["password"] is not None and self.cleaned_data["password"] != "" and self.cleaned_data["password"] == self.cleaned_data["password_confirmation"]:
            password = self.cleaned_data["password"]

        member = Member.create_member(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            username=self.cleaned_data["email"],
            password=password,
            commit=commit,
            instance=self.instance,
        )

        member.phone = self.cleaned_data["phone"]
        member.emergency_phone_primary = self.cleaned_data["emergency_phone_primary"]
        member.emergency_phone_secondary = self.cleaned_data["emergency_phone_secondary"]
        member.is_organization_admin = self.cleaned_data["is_organization_admin"]
        member.license = self.cleaned_data["license"]
        member.birthday = self.cleaned_data["birthday"]
        member.save(update_fields=self.Meta.fields)

        return member


class MassUploadForm(forms.Form):
    member_data = forms.FileField()
