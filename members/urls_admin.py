from django.urls import path

from . import views_admin

app_name = "members"
urlpatterns = [
    path("members", views_admin.MemberListView.as_view(), name="members_index"),
    path("members/add", views_admin.MemberAddView.as_view(), name="members_add"),
    path("members/add/bulk", views_admin.MassUploadView.as_view(), name="members_add_bulk"),
    path("members/edit/<int:pk>", views_admin.MemberEditView.as_view(), name="members_edit"),
    path("members/delete/<int:pk>", views_admin.MemberDeleteView.as_view(), name="members_delete"),
]
