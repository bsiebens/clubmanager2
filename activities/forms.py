from django import forms
from .models import GameType


class GameTypeForm(forms.ModelForm):
    class Meta:
        model = GameType
        fields = ["name"]
        localized_fields = fields
