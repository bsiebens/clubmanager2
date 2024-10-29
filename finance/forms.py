from django import forms
from django.forms import inlineformset_factory

from .models import LineItem, Order, OrderFormItem, OrderForm


class OrderFormItemForm(forms.ModelForm):
    class Meta:
        model = OrderFormItem
        fields = "__all__"
        localized_fields = fields


class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = "__all__"
        localized_fields = fields


OrderFormItemFormSet = inlineformset_factory(OrderForm, OrderFormItem, form=OrderFormItemForm, fields=["description", "unit_price",
                                                                                                       "unit_price_type", "member_required",
                                                                                                       "team", "role"],
                                             extra=1,
                                             can_delete=True)
OrderLineItemFormSet = inlineformset_factory(Order, LineItem, form=LineItemForm, fields=["number"], extra=1, can_delete=True)
