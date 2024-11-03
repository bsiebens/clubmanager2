#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

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

class LineItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        for form in self.forms:
            order = form.cleaned_data.get("order")
            order_item = form.cleaned_data.get("order_form_item")

            if order and order.order_form != order_item.order_form:
                form.add_error("order_form_item", "Item is of a different order")


                print(order.order_form)
                print(order_item.order_form)
                print(order.order_form == order_item.order_form)

                if order.order_form != order_item.order_form:
                    print("RAISING ERROR")
                    raise forms.ValidationError(_("Item is of a different order form than the selected form"), code="invalid")


OrderFormItemFormSet = inlineformset_factory(OrderForm, OrderFormItem, form=OrderFormItemForm,
                                             fields=["description", "unit_price", "unit_price_type", "member_required", "team", "role", ], extra=1,
                                             can_delete=True)
OrderLineItemFormSet = inlineformset_factory(Order, LineItem, form=LineItemForm, fields=["number", "order_form_item", "member"], extra=1,
                                             can_delete=True, formset=LineItemFormSet)
