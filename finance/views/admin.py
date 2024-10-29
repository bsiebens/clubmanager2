from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.forms import BaseForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from clubmanager.views import MessagesDeniedMixin
from finance.filters import OrderFormFilter
from finance.forms import OrderFormItemFormSet
from finance.models import Sponsor, OrderForm


class SponsorListView(MessagesDeniedMixin, ListView):
    model = Sponsor
    paginate_by = 25
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the sponsor list")


class SponsorAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView):
    model = Sponsor
    fields = ["name", "url", "logo"]
    success_message = _("Sponsor <strong>%(name)s</strong> added successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    permission_required = "finance"
    permission_denied_message = SponsorListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_initial(self) -> dict:
        initial_data = super().get_initial()
        initial_data["start_date"] = timezone.now().date()
        return initial_data


class SponsorEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView):
    model = Sponsor
    fields = ["name", "url", "logo"]
    success_message = _("Sponsor <strong>%(name)s</strong> updated successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    permission_required = "finance"
    permission_denied_message = SponsorListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class SponsorDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView):
    model = Sponsor
    success_url = reverse_lazy("clubmanager_admin:finance:sponsors_index")
    success_message = _("Sponsor <strong>%(name)s</strong> deleted successfully")
    permission_required = "finance"
    permission_denied_message = SponsorListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OrderFormListView(MessagesDeniedMixin, FilterView):
    filterset_class = OrderFormFilter
    paginate_by = 25
    permission_required = "finance"
    permission_denied_message = _("You do not have sufficient access rights to access the form list")


class OrderFormAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView):
    model = OrderForm
    fields = ["name", "start_date", "end_date", "allow_only_one_per_member"]
    success_message = _("Form <strong>%(name)s</strong> added successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:forms_index")
    permission_required = "finance"
    permission_denied_message = OrderFormListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["orderformitems"] = OrderFormItemFormSet(self.request.POST)
        else:
            context["orderformitems"] = OrderFormItemFormSet()

        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        context = self.get_context_data()
        order_form_items = context["orderformitems"]

        with transaction.atomic():
            self.object = form.save()
            if order_form_items.is_valid():
                order_form_items.instance = self.object
                order_form_items.save()

        return super().form_valid(form)


class OrderFormEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView):
    model = OrderForm
    fields = ["name", "start_date", "end_date", "allow_only_one_per_member"]
    success_message = _("Form <strong>%(name)s</strong> updated successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:forms_index")
    permission_required = "finance"
    permission_denied_message = OrderFormListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["orderformitems"] = OrderFormItemFormSet(self.request.POST, instance=self.object)
        else:
            context["orderformitems"] = OrderFormItemFormSet(instance=self.object)

        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        context = self.get_context_data()
        order_form_items = context["orderformitems"]

        with transaction.atomic():
            self.object = form.save()
            if order_form_items.is_valid():
                order_form_items.save()

        return super().form_valid(form)


class OrderFormDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView):
    model = OrderForm
    success_url = reverse_lazy("clubmanager_admin:finance:forms_index")
    success_message = _("Form <strong>%(name)s</strong> deleted successfully")
    permission_required = "finance"
    permission_denied_message = OrderFormListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.name)


class OrderListView(MessagesDeniedMixin, FilterView): ...


class OrderAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView): ...


class OrderEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView): ...


class OrderDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView): ...
