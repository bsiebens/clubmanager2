from django.urls import include, path

from . import views as clubmanager_views

app_name = "clubmanager_admin"
urlpatterns = [
    path("", clubmanager_views.index_admin, name="index"),
    path("members/", include("members.urls_admin")),
]
