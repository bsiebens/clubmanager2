from django.contrib import admin

from .models import Season, NumberPool, Team, TeamMembership, TeamPicture, TeamRole


class TeamPictureInlineAdmin(admin.TabularInline):
    model = TeamPicture
    extra = 0


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ["start_date", "end_date", "current_season"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["start_date", "end_date"]}],
    ]


@admin.register(NumberPool)
class NumberPoolAdmin(admin.ModelAdmin):
    list_display = ["name", "enforce_unique"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["name", "enforce_unique"]}],
    ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "short_name", "slug", "type", "created", "modified"]
    list_filter = ["type", "number_pool"]
    search_fields = ["name"]
    readonly_fields = ["slug"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["name", "short_name", "type", "number_pool"]}],
        ["OTHER", {"fields": ["slug"]}],
    ]
    inlines = [TeamPictureInlineAdmin]


@admin.register(TeamRole)
class TeamRoleAdmin(admin.ModelAdmin):
    list_display = ["name", "abbreviation", "staff_role", "admin_role", "sort_order"]
    list_filter = ["staff_role", "admin_role"]
    search_fields = ["name", "abbreviation"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["name", "abbreviation", "staff_role", "admin_role"]}],
        ["OTHER", {"fields": ["sort_order"]}],
    ]


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ["member", "team", "season", "role"]
    list_filter = ["team", "season", "role"]
    search_fields = ["member__user__first_name", "member__user__last_name", "team__name", "team__short_name", "role__name", "role__abbreviation"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["member", "team", "season", "role"]}],
        ["OTHER", {"fields": ["number", "captain", "assistant_captain"]}],
    ]
    raw_id_fields = ["member"]
