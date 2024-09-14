from rest_framework import routers

from frontend.api import SponsorViewSet
from teams.api import TeamMembersViewSet

router = routers.DefaultRouter()
router.register(r"sponsors", SponsorViewSet)
router.register(r"teams", TeamMembersViewSet)
