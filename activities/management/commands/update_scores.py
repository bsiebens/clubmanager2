from django.core.management.base import BaseCommand, CommandError, CommandParser

from activities.models import Game
from django.db.models import Q
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = "Fetches updates for games with a start date in the last 3 hours based on their competition parameters"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--hours", action="store", default=3, type=int, help="Change the hour limit to the specified number of hours")

    def handle(self, *args, **options) -> None:
        hour_limit = options["hours"]

        games = Game.objects.filter(Q(live=True) | Q(date__lte=timezone.now(), date__gte=timezone.now() - datetime.timedelta(hours=hour_limit)))
        for game in games:
            game.update_game_information()

            if game.competition is not None:
                self.stdout.write(self.style.SUCCESS('Game information updated for "%s"' % game))
            else:
                self.stdout.write(self.style.WARNING('Skipped "%s" - no competition set' % game))
