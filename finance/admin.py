#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Sponsor, OrderFormItem, LineItem, OrderForm, Order


class OrderFormItemInlineAdmin(admin.TabularInline):
    model = OrderFormItem
    extra = 0
    fields = ["description", "unit_price", "unit_price_type", "member_required", "team", "role"]


class LineItemInlineAdmin(admin.TabularInline):
    model = LineItem
    extra = 0
    fields = ["number", "order_form_item", "member", "display_unit_price"]
    raw_id_fields = ["member"]
    readonly_fields = ["display_unit_price"]

    def get_formset(self, request, obj = None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        if obj is not None:
            formset.form.base_fields["order_form_item"].widget.queryset = OrderFormItem.objects.filter(order_form=obj.order_form)

        return formset


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "start_date", "end_date", "active"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["name", "url", "logo"]}],
        ["DATE INFORMATION", {"fields": ["start_date", "end_date"]}],
    ]


@admin.register(OrderForm)
class OrderFormAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "allow_only_one_per_member", "active", "created", "modified"]
    list_filter = ["allow_only_one_per_member"]
    search_fields = ["name"]
    fieldsets = [["GENERAL INFORMATION", {"fields": ["name", ("start_date", "end_date"), "allow_only_one_per_member"]}]]
    inlines = [OrderFormItemInlineAdmin]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def display_order(self, obj: Order) -> str:
        return f"Order {obj.uuid}"

    def display_members(self, obj: Order) -> str:
        return mark_safe("<br />".join([f"{member.first_name} {member.last_name}" for member in obj.members_in_order()]))

    def display_price(self, obj: Order) -> str:
        return mark_safe(f"{obj.total()} {settings.CLUB_DEFAULT_CURRENCY_ENTITY}")

    display_order.short_description = "Order"
    display_members.short_description = "Members"
    display_price.short_description = "Price"

    list_display = ["display_order", "status", "member", "display_members", "display_price", "created", "modified"]
    list_filter = ["status"]
    # noinspection PyUnresolvedReferences
    search_fields = [
        "lineitems__order_form_item__description",
        "member__user__first_name",
        "member__user__last_name",
        "lineitems__member__user__first_name",
        "lineitems__member__user__last_name",
        "order_form__name",
    ]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["status", "member", "order_form"]}],
    ]
    raw_id_fields = ["order_form", "member"]
    inlines = [LineItemInlineAdmin]
