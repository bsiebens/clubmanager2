from django.urls import path
from django.views.generic import RedirectView

app_name = "clubmanager"
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="clubmanager_admin:index"), name="index"),
    # path("", clubmanager_views.index, name="index"),
]
