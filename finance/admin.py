from django.contrib import admin

from .models import Sponsor, Invoice, Material, LineItem


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "start_date", "end_date", "active"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["name", "url", "logo"]}],
        ["DATE INFORMATION", {"fields": ["start_date", "end_date"]}],
    ]


admin.site.register(Invoice)
admin.site.register(Material)
admin.site.register(LineItem)
