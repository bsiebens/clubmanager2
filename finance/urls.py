from django.urls import path

from . import views_admin

app_name = "finance"
urlpatterns = [
    path("sponsors", views_admin.SponsorListView.as_view(), name="sponsors_index"),
    path("sponsors/add", views_admin.SponsorAddView.as_view(), name="sponsors_add"),
    path("sponsors/edit/<int:pk>", views_admin.SponsorEditView.as_view(), name="sponsors_edit"),
    path("sponsors/delete/<int:pk>", views_admin.SponsorDeleteView.as_view(), name="sponsors_delete"),
    # path("materials", views_admin.MaterialListView.as_view(), name="materials_index"),
    # path("materials/add", views_admin.MaterialAddView.as_view(), name="materials_add"),
    # path("materials/edit/<int:pk>", views_admin.MaterialEditView.as_view(), name="materials_edit"),
    # path("materials/delete/<int:pk>", views_admin.MaterialDeleteView.as_view(), name="materials_delete"),
    # path("orders", views_admin.OrderListView.as_view(), name="orders_index"),
    # path("orders/add", views_admin.OrderAddView.as_view(), name="orders_add"),
    # path("orders/edit/<int:pk>", views_admin.OrderEditView.as_view(), name="orders_edit"),
    # path("orders/delete/<int:pk>", views_admin.OrderDeleteView.as_view(), name="orders_delete"),
]
