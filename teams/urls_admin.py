from django.urls import path

from . import views_admin

app_name = "teams"
urlpatterns = [
    path("teams", views_admin.TeamsListView.as_view(), name="teams_index"),
    path("teams/add", views_admin.TeamsAddView.as_view(), name="teams_add"),
    path("teams/edit/<int:pk>", views_admin.TeamsEditView.as_view(), name="teams_edit"),
    path("teams/delete/<int:pk>", views_admin.TeamsDeleteView.as_view(), name="teams_delete"),
    path("seasons", views_admin.SeasonListView.as_view(), name="seasons_index"),
    path("seasons/add", views_admin.SeasonAddView.as_view(), name="seasons_add"),
    path("seasons/delete/<int:pk>", views_admin.SeasonDeleteView.as_view(), name="seasons_delete"),
    path("numberpools", views_admin.NumberPoolListView.as_view(), name="numberpools_index"),
    path("numberpools/add", views_admin.NumberPoolAddView.as_view(), name="numberpools_add"),
    path("numberpools/delete/<int:pk>", views_admin.NumberPoolDeleteView.as_view(), name="numberpools_delete"),
    path("teamroles", views_admin.TeamRoleListView.as_view(), name="teamroles_index"),
    path("teamroles/add", views_admin.TeamRoleAddView.as_view(), name="teamroles_add"),
    path("teamroles/edit/<int:pk>", views_admin.TeamRoleEditView.as_view(), name="teamroles_edit"),
    path("teamroles/delete/<int:pk>", views_admin.TeamRoleDeleteView.as_view(), name="teamroles_delete"),
    path("teammembers", views_admin.TeamMembersListView.as_view(), name="teammembers_index"),
    path("teammembers/add", views_admin.TeamMembersAddView.as_view(), name="teammembers_add"),
    path("teammembers/edit/<int:pk>", views_admin.TeamMembersEditView.as_view(), name="teammembers_edit"),
    path("teammembers/delete/<int:pk>", views_admin.TeamMembersDeleteView.as_view(), name="teammembers_delete"),
]
