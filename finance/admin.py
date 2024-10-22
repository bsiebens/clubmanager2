from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import LineItem, Material, Order, Sponsor


class LineItemInlineAdmin(admin.TabularInline):
    model = LineItem
    extra = 0
    fields = ["number", "material", "member", "price"]
    raw_id_fields = ["member"]
    readonly_fields = ["price"]


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "start_date", "end_date", "active"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["name", "url", "logo"]}],
        ["DATE INFORMATION", {"fields": ["start_date", "end_date"]}],
    ]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    def display_price(self, obj):
        unit = "&percnt;" if obj.price_type == Material.PriceType.PERCENTAGE else settings.CLUB_DEFAULT_CURRENCY_ENTITY

        return mark_safe("{price} {unit}".format(price=obj.price, unit=unit))

    display_price.short_description = "Price"

    list_display = ["description", "display_price", "team", "role"]
    search_fields = ["description"]
    list_filter = ["team", "role"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["description", "price", "price_type"]}],
        ["TEAM INFORMATION", {"fields": ["team", "role"]}],
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def display_order(self, obj):
        return "Order {uuid}".format(uuid=obj.uuid)

    display_order.short_description = "Order"

    def display_members(self, obj):
        members = obj.lineitem_set.all().values("member__user__first_name", "member__user__last_name").distinct()
        members = ["{first_name} {last_name}".format(first_name=member["member__user__first_name"], last_name=member["member__user__last_name"]) for member in members]

        return mark_safe("<br />".join(members))

    display_members.short_description = "Members"

    def display_price(self, obj):
        return mark_safe("{total} {unit}".format(total=obj.total(), unit=settings.CLUB_DEFAULT_CURRENCY_ENTITY))

    display_price.short_description = "Price"

    list_display = ["display_order", "display_members", "display_price", "status", "season", "created", "modified"]
    list_filter = ["status", "season"]
    readonly_fields = ["created", "modified"]
    search_fields = ["lineitem__member__user__first_name", "lineitem__member__user__last_name"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["status", "season", ("created", "modified")]}],
    ]
    inlines = [LineItemInlineAdmin]
