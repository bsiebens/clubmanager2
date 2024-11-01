#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

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

    def clean(self) -> dict:
        cleaned_data = super().clean()

        order_form_item_order_form = cleaned_data.get("order_form_item").order_form
        order_form = cleaned_data.get("order").order_form


OrderFormItemFormSet = inlineformset_factory(
    OrderForm,
    OrderFormItem,
    form=OrderFormItemForm,
    fields=[
        "description",
        "unit_price",
        "unit_price_type",
        "member_required",
        "team",
        "role",
    ],
    extra=1,
    can_delete=True,
)
OrderLineItemFormSet = inlineformset_factory(
    Order,
    LineItem,
    form=LineItemForm,
    fields=["number", "order_form_item", "member"],
    extra=1,
    can_delete=True,
)
