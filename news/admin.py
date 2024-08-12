from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin
from .models import NewsItem


@admin.register(NewsItem)
class NewsAdmin(ObjectPermissionsModelAdmin):
    list_display = ["title", "slug"]
