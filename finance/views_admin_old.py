#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rules.contrib.views import PermissionRequiredMixin

from .models import Sponsor


class SponsorListView(PermissionRequiredMixin, ListView):
    model = Sponsor
    paginate_by = 50
    permission_required = "finance"
    permission_denied_message = _(
        "You do not have sufficient access rights to access the sponsor list"
    )

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))


class SponsorAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Sponsor
    fields = ["name", "url", "logo", "start_date", "end_date"]
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> added succesfully")
    permission_required = "finance"
    permission_denied_message = _(
        "You do not have sufficient access rights to access the sponsor list"
    )

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_initial(self) -> dict[str, Any]:
        initial_data = super(SponsorAddView, self).get_initial()

        initial_data["start_date"] = timezone.now().date()

        return initial_data


class SponsorEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Sponsor
    fields = ["name", "url", "logo", "start_date", "end_date"]
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> updated succesfully")
    permission_required = "finance"
    permission_denied_message = _(
        "You do not have sufficient access rights to access the sponsor list"
    )

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class SponsorDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Sponsor
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> deleted succesfully")
    permission_required = "finance"
    permission_denied_message = _(
        "You do not have sufficient access rights to access the sponsor list"
    )

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


# class MaterialListView(PermissionRequiredMixin, ListView):
#     model = Material
#     paginate_by = 50
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access rights to access the cost item list")
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#
# class MaterialAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Material
#     fields = ["description", "price", "price_type", "team", "role"]
#     success_url = reverse_lazy("clubmanager_admin:finance:materials_index")
#     success_message = _("Cost item <strong>%(name)s</strong> added succesfully")
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access rights to access the cost item list")
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#     def get_success_message(self, cleaned_data: dict[str, str]) -> str:
#         return self.success_message % dict(cleaned_data, name=self.object.description)
#
#
# class MaterialEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Material
#     fields = ["description", "price", "price_type", "team", "role"]
#     success_url = reverse_lazy("clubmanager_admin:finance:materials_index")
#     success_message = _("Cost item <strong>%(name)s</strong> updated succesfully")
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access rights to access the cost item list")
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#     def get_success_message(self, cleaned_data: dict[str, str]) -> str:
#         return self.success_message % dict(cleaned_data, name=self.object.description)
#
#
# class MaterialDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Material
#     success_url = reverse_lazy("clubmanager_admin:finance:materials_index")
#     success_message = _("Cost item <strong>%(name)s</strong> deleted succesfully")
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access rights to access the cost item list")
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#     def get_success_message(self, cleaned_data: dict[str, str]) -> str:
#         return self.success_message % dict(cleaned_data, name=self.object.description)
#
#
# class OrderListView(PermissionRequiredMixin, FilterView):
#     filterset_class = OrderFilter
#     paginate_by = 25
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access rights to access the registration list")
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#     def get_filterset_kwargs(self, filterset_class) -> dict[str, Any]:
#         kwargs = super(OrderListView, self).get_filterset_kwargs(filterset_class)
#
#         if kwargs["data"] is None:
#             filter_values = {}
#         else:
#             filter_values = kwargs["data"].dict()
#
#         if not filter_values:
#             filter_values.update({"season": str(Season.get_season_id())})
#
#         kwargs["data"] = filter_values
#
#         return kwargs
#
#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super(OrderListView, self).get_context_data(**kwargs)
#         context["new"] = 0
#         context["submitted"] = 0
#         context["invoiced"] = 0
#         context["payed"] = 0
#
#         counts = Order.objects.filter(season=Season.get_season_id()).values("status").annotate(Count("status"))
#         for count in counts:
#             match count["status"]:
#                 case 0:
#                     context["new"] = count["status__count"]
#                 case 1:
#                     context["submitted"] = count["status__count"]
#                 case 2:
#                     context["invoiced"] = count["status__count"]
#                 case 3:
#                     context["payed"] = count["status__count"]
#
#         return context
#
#
# class OrderAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Order
#     fields = ["season"]
#     success_url = reverse_lazy("clubmanager_admin:finance:orders_index")
#     success_message = _("Registration <strong>%(name)s</strong> added succesfully")
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access righs to access the registration list")
#
#     def get_success_message(self, cleaned_data: dict[str, str]) -> str:
#         return self.success_message % dict(cleaned_data, name=self.object.uuid)
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#     def get_context_data(self, **kwargs) -> dict[str, Any]:
#         context = super(OrderAddView, self).get_context_data(**kwargs)
#
#         if self.request.POST:
#             print(self.request.POST)
#             context["lineitems"] = OrderLineItemFormSet(self.request.POST)
#         else:
#             context["lineitems"] = OrderLineItemFormSet()
#
#         return context
#
#     def form_valid(self, form: BaseForm) -> HttpResponse:
#         context = self.get_context_data()
#
#         lineitems = context["lineitems"]
#         with transaction.atomic():
#             self.object = form.save()
#
#             print(self.object)
#
#             if lineitems.is_valid():
#                 lineitems.instance = self.object
#
#                 print(lineitems)
#                 print(lineitems.instance)
#
#                 lineitems.save()
#
#         return super(OrderAddView, self).form_valid(form)
#
#
# class OrderEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Order
#     fields = ["season"]
#     success_url = reverse_lazy("clubmanager_admin:finance:orders_index")
#     success_message = _("Registration <strong>%(name)s</strong> updated succesfully")
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access righs to access the registration list")
#
#     def get_success_message(self, cleaned_data: dict[str, str]) -> str:
#         return self.success_message % dict(cleaned_data, name=self.object.uuid)
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#     def get_context_data(self, **kwargs) -> dict[str, Any]:
#         context = super(OrderEditView, self).get_context_data(**kwargs)
#
#         if self.request.POST:
#             print(self.request.POST)
#             context["lineitems"] = OrderLineItemFormSet(self.request.POST, instance=self.object)
#         else:
#             context["lineitems"] = OrderLineItemFcounormSet(instance=self.object)
#
#         return context
#
#     def form_valid(self, form: BaseForm) -> HttpResponse:
#         context = self.get_context_data()
#
#         lineitems = context["lineitems"]
#         with transaction.atomic():
#             self.object = form.save()
#
#             if lineitems.is_valid():
#                 lineitems.save()
#
#         return super(OrderEditView, self).form_valid(form)
#
#
# class OrderDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Order
#     success_url = reverse_lazy("clubmanager_admin:finance:orders_index")
#     success_message = _("Registration <strong>%(name)s</strong> deleted succesfully")
#     permission_required = "finance"
#     permission_denied_message = _("You do not have sufficient access rights to access the registration list")
#
#     def handle_no_permission(self) -> HttpResponseRedirect:
#         messages.error(self.request, self.get_permission_denied_message())
#         return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))
#
#     def get_success_message(self, cleaned_data: dict[str, str]) -> str:
#         return self.success_message % dict(cleaned_data, name=self.object.uuid)
