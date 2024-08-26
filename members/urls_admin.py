from django.urls import path

from . import views_admin

app_name = "members"
urlpatterns = [
    path("members/", views_admin.MemberListView.as_view(), name="members_index"),
    path("members/add/", views_admin.MemberAddView.as_view(), name="members_add"),
    path("members/edit/<int:pk>/", views_admin.MemberEditView.as_view(), name="members_edit"),
    path("members/delete/<int:pk>/", views_admin.MemberDeleteView.as_view(), name="members_delete"),
    path("families/", views_admin.FamilyListView.as_view(), name="families_index"),
    path("families/add/", views_admin.FamilyAddView.as_view(), name="families_add"),
    path("families/edit/<int:pk>/", views_admin.FamilyEditView.as_view(), name="families_edit"),
    path("families/delete/<int:pk>/", views_admin.FamilyDeleteView.as_view(), name="families_delete"),
]
