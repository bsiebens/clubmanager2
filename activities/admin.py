from django.contrib import admin

from .models import Competition, Opponent, Game, GameType


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
    list_filter = ["team", "season", "opponent", "location", "competition", "game_type"]
    search_fields = ["team__name", "opponent__name", "location"]
    list_display = ["date", "team", "opponent", "season", "location", "competition", "game_id", "game_type"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["team", "opponent", "date", "location", "game_type"]}],
        ["COMPETITION INFORMATION", {"fields": ["competition", "game_id", "live", "score_team", "score_opponent"]}],
    ]
    list_editable = ["competition", "game_id"]


admin.site.register(Competition)
admin.site.register(GameType)
