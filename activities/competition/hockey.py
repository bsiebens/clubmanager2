from .base import Competition, GameInformation
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


class RBIHF(Competition):
    def __init__(self):
        self.url = "https://www.rbihf.be/game/"

    def fetch_game_information(self, game_id: int):
        url = urljoin(self.url, str(game_id))

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        print(page)
