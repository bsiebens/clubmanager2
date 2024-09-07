from typing import TypedDict


class GameInformation(TypedDict):
    live: bool
    home_score: int
    away_score: int


class Competition:
    url: str

    def __init__(self):
        self.url = "http://localhost"

    def fetch_game_information(self, game_id: str) -> dict[str, bool | int]:
        return {"live": False, "home_score": 0, "away_score": 0}
