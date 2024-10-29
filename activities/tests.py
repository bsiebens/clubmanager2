from django.test import TestCase
from django.utils import timezone

from teams.models import Season, Team
from .models import Game, Opponent, GameType


class GameModelTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.team = Team.objects.create(name="Team", logo="logo.jpg")
        self.opponent = Opponent.objects.create(name="Opponent", logo="opponent.jpg")
        self.season = Season.get_season(date=timezone.now().date())
        self.game_type = GameType.objects.get(name="Friendly Game")
        self.game = Game.objects.create(team=self.team, game_type=self.game_type, opponent=self.opponent, date=timezone.now())

    def test_game_no_season(self):
        self.assertEqual(self.game.season, self.season)

    def test_game_string(self):
        self.assertEqual(str(self.game), "Team vs Opponent")

    def test_home_game(self):
        self.assertTrue(self.game.is_home_game)

        self.game.location = "Somewhere else"
        self.game.save()

        self.assertFalse(self.game.is_home_game)
