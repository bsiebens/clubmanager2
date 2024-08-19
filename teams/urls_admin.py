from django.urls import path

from . import views_admin

app_name = "teams"
urlpatterns = [
    path("teams/", views_admin.TeamsListView.as_view(), name="index"),
    path("seasons/", views_admin.SeasonListView.as_view(), name="seasons_index"),
    path("seasons/add/", views_admin.SeasonAddView.as_view(), name="seasons_add"),
    path("seasons/delete/<int:pk>/", views_admin.SeasonDeleteView.as_view(), name="seasons_delete"),
    path("numberpools/", views_admin.NumberPoolListView.as_view(), name="numberpools_index"),
    path("numberpools/add/", views_admin.NumberPoolAddView.as_view(), name="numberpools_add"),
    path("numberpools/delete/<int:pk>/", views_admin.NumberPoolDeleteView.as_view(), name="numberpools_delete"),
    path("teamroles/", views_admin.TeamRoleListView.as_view(), name="teamroles_index"),
    path("teamroles/add/", views_admin.TeamRoleAddView.as_view(), name="teamroles_add"),
    path("teamroles/edit/<int:pk>/", views_admin.TeamRoleEditView.as_view(), name="teamroles_edit"),
    path("teamroles/delete/<int:pk>/", views_admin.TeamRoleDeleteView.as_view(), name="teamroles_delete"),
]


""" from django.urls import path

from . import views_admin

app_name = "news"
urlpatterns = [
    path("editors/", views_admin.EditorListView.as_view(), name="editors_index"),
    path("editors/add/", views_admin.EditorAddView.as_view(), name="editors_add"),
    path("editors/delete/<int:pk>", views_admin.EditorDeleteView.as_view(), name="editors_delete"),
    path("news/", views_admin.NewsListView.as_view(), name="news_index"),
    path("news/add/", views_admin.NewsAddView.as_view(), name="news_add"),
    path("news/edit/<int:pk>/", views_admin.NewsEditView.as_view(), name="news_edit"),
    path("news/preview/<int:pk>/", views_admin.NewsPreviewView.as_view(), name="news_preview"),
    path("news/delete/<int:pk>/", views_admin.NewsDeleteView.as_view(), name="news_delete"),
    path("news/release/<int:pk>/", views_admin.release_newsitem, name="news_release"),
    path("news/state/<int:pk>/<str:status>/", views_admin.update_status_newsitem, name="news_update_status"),
]
 """
