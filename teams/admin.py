from django.contrib import admin

from .models import Season, NumberPool, Team, TeamMembership, TeamPicture, TeamRole

admin.site.register(Season)
admin.site.register(NumberPool)
admin.site.register(Team)
admin.site.register(TeamMembership)
admin.site.register(TeamPicture)
admin.site.register(TeamRole)
