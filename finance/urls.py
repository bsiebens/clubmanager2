#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

from django.urls import path

from .views import admin

app_name = "finance"
urlpatterns = [
    path("sponsors", admin.SponsorListView.as_view(), name="sponsors_index"),
    path("sponsors/add", admin.SponsorAddView.as_view(), name="sponsors_add"),
    path("sponsors/edit/<int:pk>", admin.SponsorEditView.as_view(), name="sponsors_edit"),
    path("sponsors/delete/<int:pk>", admin.SponsorDeleteView.as_view(), name="sponsors_delete"),
    path("forms", admin.OrderFormListView.as_view(), name="forms_index"),
    path("forms/add", admin.OrderFormAddView.as_view(), name="forms_add"),
    path("forms/edit/<int:pk>", admin.OrderFormEditView.as_view(), name="forms_edit"),
    path("forms/delete/<int:pk>", admin.OrderFormDeleteView.as_view(), name="forms_delete"),
    path("orders", admin.OrderListView.as_view(), name="orders_index"),
    path("orders/add", admin.OrderAddView.as_view(), name="orders_add"),
    path("orders/edit/<int:pk>", admin.OrderEditView.as_view(), name="orders_edit"),
    path("orders/delete/<int:pk>", admin.OrderDeleteView.as_view(), name="orders_delete"),
]
