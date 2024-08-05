from django.urls import path

from . import views_admin

app_name = "members"
urlpatterns = [
    path("", views_admin.MemberListView.as_view(), name="index"),
    path("delete/<int:pk>/", views_admin.MemberDeleteView.as_view(), name="delete"),
]
