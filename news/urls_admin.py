from django.urls import path

from . import views_admin

app_name = "news"
urlpatterns = [
    path("editors/", views_admin.EditorListView.as_view(), name="editors_index"),
    path("editors/add/", views_admin.EditorAddView.as_view(), name="editors_add"),
    path("editors/delete/<int:pk>", views_admin.EditorDeleteView.as_view(), name="editors_delete"),
    path("news/", views_admin.NewsListView.as_view(), name="news_index"),
]

""" from django.urls import path

from . import views_admin

app_name = "members"
urlpatterns = [
    path("", views_admin.MemberListView.as_view(), name="index"),
    path("add/", views_admin.MemberAddView.as_view(), name="add"),
    path("edit/<int:pk>/", views_admin.MemberEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", views_admin.MemberDeleteView.as_view(), name="delete"),
]
 """
