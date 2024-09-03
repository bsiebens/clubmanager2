from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin
from markdownx.admin import MarkdownxModelAdmin
from .models import NewsItem, Picture


class PictureInlineAdmin(admin.TabularInline):
    model = Picture
    extra = 0


@admin.register(NewsItem)
class NewsAdmin(ObjectPermissionsModelAdmin, MarkdownxModelAdmin):
    list_display = ["title", "author_name", "status", "type", "publish_on", "modified"]
    date_hierarchy = "publish_on"
    list_filter = ["status", "type", "modified"]
    search_fields = ["title", "text"]
    inlines = [PictureInlineAdmin]
    raw_id_fields = ["author"]
    fieldsets = [
        ["GENERAL INFORMATION", {"fields": ["title", "text"]}],
        ["METADATA", {"fields": ["author", ("status", "type"), "publish_on", "teams"]}],
        ["OTHER", {"fields": ["slug"]}],
    ]
    readonly_fields = ["slug"]
    filter_horizontal = ["teams"]
