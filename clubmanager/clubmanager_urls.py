from django.urls import include, path

from . import views as clubmanager_views

app_name = "clubmanager"
urlpatterns = [
    path("", clubmanager_views.index, name="index"),
]
