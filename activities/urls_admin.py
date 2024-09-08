from django.urls import path

from . import views_admin

app_name = "activities"
urlpatterns = [
    path("opponents", views_admin.OpponentsListView.as_view(), name="opponents_index"),
    path("opponents/add", views_admin.OpponentsAddView.as_view(), name="opponents_add"),
    path("opponents/edit/<int:pk>", views_admin.OpponentsEditView.as_view(), name="opponents_edit"),
    path("opponents/delete/<int:pk>", views_admin.OpponentsDeleteView.as_view(), name="opponents_delete"),
    path("games", views_admin.GamesListView.as_view(), name="games_index"),
    path("games/add", views_admin.GamesAddView.as_view(), name="games_add"),
    path("games/edit/<int:pk>", views_admin.GamesEditView.as_view(), name="games_edit"),
    path("games/delete/<int:pk>", views_admin.GamesDeleteView.as_view(), name="games_delete"),
    path("games/view/<int:pk>", views_admin.GamePreviewView.as_view(), name="games_view"),
    path("games/refresh/<int:pk>", views_admin.update_game_information, name="games_refresh"),
]
