from django.urls import path

from . import views_admin

app_name = "frontend"
urlpatterns = [
    path("sponsors", views_admin.SponsorListView.as_view(), name="sponsors_index"),
    path("sponsors/add", views_admin.SponsorAddView.as_view(), name="sponsors_add"),
    path("sponsors/edit/<int:pk>", views_admin.SponsorEditView.as_view(), name="sponsors_edit"),
    path("sponsors/delete/<int:pk>", views_admin.SponsorDeleteView.as_view(), name="sponsors_delete"),
]
