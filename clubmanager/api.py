from rest_framework import routers

from activities.api import GameViewSet
from finance.api import SponsorViewSet
from news.api import NewsItemViewSet
from teams.api import TeamsViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r"sponsors", SponsorViewSet)
router_v1.register(r"teams", TeamsViewSet)
router_v1.register(r"games", GameViewSet, basename="")
router_v1.register(r"news", NewsItemViewSet)

router_v2 = routers.DefaultRouter()
router_v2.register(r"sponsors", SponsorViewSet)
router_v2.register(r"teams", TeamsViewSet)
router_v2.register(r"games", GameViewSet, basename="")
router_v2.register(r"news", NewsItemViewSet)
