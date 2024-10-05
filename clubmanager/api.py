from rest_framework import routers

from frontend.api import SponsorViewSet
from teams.api import TeamsViewSet
from activities.api import GameViewSet
from news.api import NewsItemViewSet

router = routers.DefaultRouter()
router.register(r"sponsors", SponsorViewSet, basename="sponsors")
router.register(r"teams", TeamsViewSet)
router.register(r"games", GameViewSet, basename="games")
router.register(r"news", NewsItemViewSet, basename="newsitems")
