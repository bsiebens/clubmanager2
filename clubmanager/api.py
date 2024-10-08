from rest_framework import routers

from finance.api import SponsorViewSet
from teams.api import TeamsViewSet
from activities.api import GameViewSet
from news.api import NewsItemViewSet

router = routers.DefaultRouter()
router.register(r"sponsors", SponsorViewSet)
router.register(r"teams", TeamsViewSet)
router.register(r"games", GameViewSet, basename="")
router.register(r"news", NewsItemViewSet)
