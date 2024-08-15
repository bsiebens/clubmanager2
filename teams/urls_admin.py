from django.urls import path

from . import views_admin

app_name = "teams"
urlpatterns = [
    path("teams/", views_admin.TeamsListView.as_view(), name="index"),
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
