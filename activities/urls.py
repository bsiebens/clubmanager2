from django.urls import path

from .views import admin

app_name = "activities"
urlpatterns = [
    path("opponents", admin.OpponentListView.as_view(), name="opponents_index"),
    path("opponents/add", admin.OpponentAddView.as_view(), name="opponents_add"),
    path("opponents/edit/<int:pk>", admin.OpponentEditView.as_view(), name="opponents_edit"),
    path("opponents/delete/<int:pk>", admin.OpponentDeleteView.as_view(), name="opponents_delete"),
    path("games", admin.GameListView.as_view(), name="games_index"),
    path("games/add", admin.GameAddView.as_view(), name="games_add"),
    path("games/edit/<int:pk>", admin.GameEditView.as_view(), name="games_edit"),
    path("games/delete/<int:pk>", admin.GameDeleteView.as_view(), name="games_delete"),
    path("games/view/<int:pk>", admin.GamePreviewView.as_view(), name="games_view"),
    path("games/refresh/<int:pk>", admin.refresh_game_information, name="games_refresh"),
    path("gametypes/", admin.GameTypeListView.as_view(), name="gametypes_index"),
    path("gametypes/add", admin.GameTypeAddView.as_view(), name="gametypes_add"),
    path("gametypes/edit/<int:pk>", admin.GameTypeEditView.as_view(), name="gametypes_edit"),
    path("gametypes/delete/<int:pk>", admin.GameTypeDeleteView.as_view(), name="gametypes_delete"),
]
