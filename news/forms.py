from django import forms
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from members.models import Member

from .models import NewsItem, Picture


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
        fields = ["title", "text", "type", "publish_on", "teams"]
        localized_fields = fields


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = "__all__"
        localized_fields = fields


NewsItemPictureFormSet = inlineformset_factory(NewsItem, Picture, form=PictureForm, fields=["picture", "main_picture"], extra=1, can_delete=True)
