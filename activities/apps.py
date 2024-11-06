#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "activities"

    def ready(self):
        from . import signals  # noqa: F401
