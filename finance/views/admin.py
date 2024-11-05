#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count
from django.forms import BaseForm, ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from notifications.signals import notify
from rules.contrib.views import permission_required

from clubmanager.views import MessagesDeniedMixin
from finance.filters import OrderFormFilter, OrderFilter
from finance.forms import OrderFormItemFormSet, OrderLineItemFormSet
from finance.models import Sponsor, OrderForm, Order
from teams.models import Season


class SponsorListView(MessagesDeniedMixin, ListView):
    model = Sponsor
    paginate_by = 25
    permission_required = "finance"
    permission_denied_message = _(
        "You do not have sufficient access rights to access the sponsor list"
    )


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
    permission_denied_message = _(
        "You do not have sufficient access rights to access the form list"
    )


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
            context["orderformitems"] = OrderFormItemFormSet(
                self.request.POST, instance=self.object
            )
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


class OrderListView(MessagesDeniedMixin, FilterView):
    filterset_class = OrderFilter
    paginate_by = 25
    permission_required = "finance"
    permission_denied_message = _(
        "You do not have sufficient access rights to access the order list"
    )

    def get_filterset_kwargs(self, filterset_class: OrderFilter) -> dict:
        current_season = Season.get_season()
        filter_values = {
            "start_date": current_season.start_date,
            "end_date": current_season.end_date,
        }
        kwargs = super().get_filterset_kwargs(filterset_class)

        if kwargs["data"] is not None:
            filter_values = kwargs["data"].dict()

        kwargs["data"] = filter_values
        return kwargs

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        current_season = Season.get_season()
        status_choices = {}

        for status in Order.OrderStatus.choices:
            context[status[1]] = 0
            context["choices"] = context.get("choices", []) + [status[1]]
            status_choices[status[0]] = status[1]

        counts = (
            Order.objects.filter(
                created__gte=current_season.start_date,
                created__lte=current_season.end_date,
            )
            .values("status")
            .annotate(Count("status"))
        )
        for count in counts:
            context[status_choices[count["status"]]] = count["status__count"]

        return context


class OrderAddView(MessagesDeniedMixin, SuccessMessageMixin, CreateView):
    model = Order
    fields = ["order_form", "member"]
    success_message = _("Order <strong>%(uuid)s</strong> added successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:orders_index")
    permission_required = "finance"
    permission_denied_message = OrderListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, uuid=self.object.uuid)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["lineitems"] = OrderLineItemFormSet()

        if self.request.POST:
            context["lineitems"] = OrderLineItemFormSet(self.request.POST)

        return context

    def form_valid(self, form: ModelForm) -> HttpResponse:
        context = self.get_context_data()
        line_items = context["lineitems"]

        with transaction.atomic():
            self.object = form.save()
            line_items.instance = self.object

            if line_items.is_valid():
                line_items.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class OrderEditView(MessagesDeniedMixin, SuccessMessageMixin, UpdateView):
    model = Order
    fields = ["order_form", "member"]
    success_message = _("Order <strong>%(uuid)s</strong> updated successfully")
    success_url = reverse_lazy("clubmanager_admin:finance:orders_index")
    permission_required = "finance"
    permission_denied_message = OrderListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, uuid=self.object.uuid)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["lineitems"] = OrderLineItemFormSet(self.request.POST, instance=self.object)
        else:
            context["lineitems"] = OrderLineItemFormSet(instance=self.object)

        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        context = self.get_context_data()
        line_items = context["lineitems"]

        with transaction.atomic():
            self.object = form.save()

            if line_items.is_valid():
                line_items.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class OrderDeleteView(MessagesDeniedMixin, SuccessMessageMixin, DeleteView):
    model = Order
    success_url = reverse_lazy("clubmanager_admin:finance:orders_index")
    success_message = _("Order <strong>%(uuid)s</strong> deleted successfully")
    permission_required = "finance"
    permission_denied_message = OrderListView.permission_denied_message

    def get_success_message(self, cleaned_data: dict) -> str:
        return self.success_message % dict(cleaned_data, uuid=self.object.uuid)


@permission_required("finance")
def order_invoiced(request, pk: int) -> HttpResponse:
    order = Order.objects.get(pk=pk)
    order.status = Order.OrderStatus.INVOICED
    order.save(update_fields=["status"])

    messages.success(request, _("Invoice created for order <strong>%(name)s</strong>" % ({"name": order.uuid})))
    notify.send(request.user, recipient=order.member.user, action_object=order, verb="invoiced", description=_("New invoice is now available"),
                url=reverse_lazy("clubmanager_admin:index"))

    return HttpResponseRedirect(reverse_lazy("clubmanager_admin:finance:orders_index"))


@permission_required("finance")
def order_payed(request, pk: int) -> HttpResponse:
    order = Order.objects.get(pk=pk)
    order.status = Order.OrderStatus.PAYED
    order.save(update_fields=["status"])

    messages.success(request, _("Order <strong>%(name)s</strong> marked as payed" % ({"name": order.uuid})))
    notify.send(request.user, recipient=order.member.user, action_object=order, verb="payed", description=_("Invoice has been marked as payed"),
                url=reverse_lazy("clubmanager_admin:index"))

    return HttpResponseRedirect(reverse_lazy("clubmanager_admin:finance:orders_index"))


@permission_required("finance")
def order_submitted(request, pk: int) -> HttpResponse:
    order = Order.objects.get(pk=pk)
    order.status = Order.OrderStatus.SUBMITTED
    order.save(update_fields=["status"])

    messages.success(request, _("Order <strong>%(name)s</strong> returned to submitted state" % ({"name": order.uuid})))
    notify.send(request.user, recipient=order.member.user, action_object=order, verb="invoiced", description=_("Invoice cancelled"),
                url=reverse_lazy("clubmanager_admin:index"))

    return HttpResponseRedirect(reverse_lazy("clubmanager_admin:finance:orders_index"))
