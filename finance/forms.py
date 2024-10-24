from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import LineItem, Order


class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = "__all__"
        localized_fields = fields


OrderLineItemFormSet = inlineformset_factory(Order, LineItem, form=LineItemForm, fields=["number", "material", "member"], extra=1, can_delete=True)
