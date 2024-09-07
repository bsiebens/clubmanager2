from activities.models import Game
from .base import CompetitionBaseClass, GameInformation
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import json


class RBIHF(CompetitionBaseClass):
    def __init__(self):
        self.url = "https://rbihf.be/modules/league/ajax/time.php"

    def update_game_information(self, game: Game) -> None:
        season = "{start}{end}".format(start=game.season.start_date.strftime("%y"), end=game.season.end_date.strftime("%y"))

        payload = {"gameNr": game.game_id, "season": season}
        headers = {
            "Cookie": "language=en",
            "Postman-Token": "clubmanager",
            "Host": "www.rbihf.be",
            "User-Agent": "PostmanRuntime/7.37.0",
            "Accept": "application/json",
            "Accept-Encoding": "gzip,deflate,br",
            "Connection": "keep-alive",
            "Referer": "https://rbihf.be/game/{gameNr}".format(gameNr=game.game_id),
            "X-Request-With": "XMLHttpRequest",
        }

        req = requests.get(self.url, params=payload, headers=headers)

        if req.status_code == 200:
            game_data = req.json()

            game.live = game_data["live"]

            if game.is_home_game:
                game.score_team = game_data["scoreA"]
                game.score_opponent = game_data["scoreB"]
            else:
                game.score_team = game_data["scoreB"]
                game.score_opponent = game_data["scoreA"]

            game.save(update_fields=["live", "score_team", "score_opponent"])
