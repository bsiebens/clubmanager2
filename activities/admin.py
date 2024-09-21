from django.contrib import admin

from .models import Competition, Opponent, Game


@admin.register(Opponent)
class OpponentAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["name", "logo"]}],
    ]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_filter = ["team", "season", "opponent", "location", "competition", "friendly_game"]
    search_fields = ["team__name", "opponent__name", "location"]
    list_display = ["date", "team", "opponent", "season", "location", "competition", "game_id", "friendly_game"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["team", "opponent", "date", "location"]}],
        ["COMPETITION INFORMATION", {"fields": ["competition", "game_id", "friendly_game", "live", "score_team", "score_opponent"]}],
    ]
    list_editable = ["competition", "game_id"]


admin.site.register(Competition)
