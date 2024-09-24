from rest_framework import routers

from frontend.api import SponsorViewSet
from teams.api import TeamsViewSet
from activities.api import GameViewSet

router = routers.DefaultRouter()
router.register(r"sponsors", SponsorViewSet)
router.register(r"teams", TeamsViewSet)
router.register(r"games", GameViewSet, basename="")
