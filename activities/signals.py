from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Game


@receiver(pre_save, sender=Game)
def set_default_location_if_missing(sender, instance: Game, *args, **kwargs):
    """If no location is set for a given game, will update the location to settings.CLUB_DEFAULT_HOME_LOCATION."""

    if instance.location is None or instance.location == "":
        instance.location = settings.CLUB_DEFAULT_HOME_LOCATION
