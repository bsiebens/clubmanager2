#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

import uuid
from decimal import Decimal

from auditlog.registry import auditlog
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from members.models import Member
from teams.models import Team, TeamRole


class Sponsor(models.Model):
    """
    Represents a Sponsor.

    Attributes:
        name (CharField): Name of the sponsor, maximum length of 250 characters.
        start_date (DateField): Date when the sponsor's logo becomes visible.
        end_date (DateField): Date when the sponsor's logo is no longer visible; can be left empty for indefinite display.
        url (URLField): Optional URL associated with the sponsor.
        logo (ImageField): Image file representing the sponsor's logo.

        created (DateTimeField): Timestamp indicating when the sponsor was created.
        modified (DateTimeField): Timestamp indicating when the sponsor was last modified.

    Methods:
        active (): Returns a boolean indicating if the sponsor is currently active, based on start and end dates.
    """

    name = models.CharField(_("name"), max_length=250)
    start_date = models.DateField(_("start date"), default=timezone.now, help_text=_("Logo will be visible as of this day"))
    end_date = models.DateField(
        _("end date"), blank=True, null=True, help_text=_("Logo will no longer be visible as of this date, leave empty to display indefinitely")
    )
    url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="sponsors/logo/")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    @admin.display(description=_("Active"), boolean=True)
    def active(self) -> bool:
        if self.end_date is not None:
            return self.start_date <= timezone.now().date() <= self.end_date

        return self.start_date <= timezone.now().date()


class OrderForm(models.Model):
    """An order form is the form that defines what people can order"""

    name = models.CharField(_("name"), max_length=250)
    start_date = models.DateField(_("start date"), default=timezone.now, help_text=_("Date on which this form becomes available"))
    end_date = models.DateField(
        _("end date"), blank=True, null=True, help_text=_("Final due data for this form, standard will be 30 days from the " "start date")
    )

    allow_only_one_per_member = models.BooleanField(
        _("one per user"), default=False, help_text="Select to allow only one form to be submitted by " "each user"
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("order form")
        verbose_name_plural = _("order forms")
        ordering = ["-start_date", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.end_date is None:
            self.end_date = timezone.now().date() + timezone.timedelta(days=30)

        super().save(*args, **kwargs)

    @property
    @admin.display(description=_("Active"), boolean=True)
    def active(self) -> bool:
        return self.start_date <= timezone.now().date() <= self.end_date


class OrderFormItem(models.Model):
    """An item is each thing that can be included on a given order. Optionally associated with a member."""

    class PriceType(models.IntegerChoices):
        AMOUNT = 0, _("amount")
        PERCENTAGE = 1, _("percentage")

    order_form = models.ForeignKey(OrderForm, on_delete=models.CASCADE, verbose_name=_("order form"), related_name="items")
    description = models.CharField(_("description"), max_length=250, blank=True)
    unit_price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)
    unit_price_type = models.IntegerField(_("type"), default=PriceType.AMOUNT, choices=PriceType.choices)

    member_required = models.BooleanField(
        _("member required"), default=False, help_text=_("Select if this item requires a member to be associated " "with it when creating an order")
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name=_("team"),
        blank=True,
        null=True,
        help_text=_("Optional, select a team for which an item should be created"),
    )
    role = models.ForeignKey(
        TeamRole,
        on_delete=models.CASCADE,
        verbose_name=_("team role"),
        blank=True,
        null=True,
        help_text=_("Optional, select a role for which an item should be created"),
    )

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ["description"]

    def __str__(self):
        if not self.description.startswith(f"{self.order_form.name} | "):
            return f"{self.order_form.name} | {self.description}"

        return self.description

    def save(self, *args, **kwargs):
        if self.team and self.role:
            self.description = f"{self.team.name} | {self.role.name}"

        elif self.team:
            self.description = self.team.name

        elif self.role:
            self.description = self.role.name

        super().save(*args, **kwargs)

    @property
    def display_unit_price(self):
        unit = "&percnt;" if self.unit_price_type == OrderFormItem.PriceType.PERCENTAGE else settings.CLUB_DEFAULT_CURRENCY_ENTITY

        return mark_safe(f"{self.unit_price} {unit}")


class Order(models.Model):
    """An order is a submitted version of an order form"""

    class OrderStatus(models.IntegerChoices):
        NEW = 0, _("New")
        SUBMITTED = 1, _("Submitted")
        INVOICED = 2, _("Invoiced")
        PAYED = 3, _("Payed")

    order_form = models.ForeignKey(OrderForm, on_delete=models.CASCADE, verbose_name=_("order form"), related_name="orders")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name=_("member"), related_name="orders")

    status = models.IntegerField(_("status"), choices=OrderStatus.choices, default=OrderStatus.NEW)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return _("Order {uuid}").format(uuid=self.uuid)

    def total(self):
        """Calculates the total amount for a given order. All lines are processed in order that they have been added to the order."""

        total = Decimal(0)

        for line in self.lineitems.all().prefetch_related():
            if line.order_form_item.unit_price_type == OrderFormItem.PriceType.PERCENTAGE:
                total = total + (total / 100 * line.order_form_item.unit_price)

            else:
                total = total + line.order_form_item.unit_price

        return round(total, 2)

    def members_in_order(self):
        members = []

        for line in self.lineitems.all().prefetch_related():
            if line.member not in members and line.member is not None:
                members.append(line.member)

        return members

    @property
    def display_total(self):
        return mark_safe(f"{self.total()} {settings.CLUB_DEFAULT_CURRENCY_ENTITY}")


class LineItem(models.Model):
    """A line item on a given order"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("order"), related_name="lineitems")
    member = models.ForeignKey(Member, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("member"))
    order_form_item = models.ForeignKey(OrderFormItem, on_delete=models.CASCADE, verbose_name=_("item"), related_name="lineitems")
    number = models.IntegerField(blank=True)

    class Meta:
        verbose_name = _("line item")
        verbose_name_plural = _("line items")
        ordering = ["number"]

    def __str__(self):
        return self.order_form_item.description

    def save(self, *args, **kwargs):
        if self.number is None or self.number == 0:
            current_max_number = self.order.lineitems.aggregate(Max("number"))["number__max"]

            if current_max_number is None:
                current_max_number = 0

            self.number = current_max_number + 10

        if self.order_form_item.member_required and self.member is None:
            raise ValidationError(_("Member is required for this order item"))

        if self.order_form_item.order_form != self.order.order_form:
            raise ValidationError(_("Order form for item does not match order form for order"))

        super().save(*args, **kwargs)

    @property
    @admin.display(description=_("Unit price"))
    def display_unit_price(self):
        return self.order_form_item.display_unit_price


auditlog.register(Order)
