from django.contrib import admin
from django.db import models, transaction
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel

from members.models import Member
from teams.models import Season, Team, TeamRole


class LineItemManager(models.Manager):
    def create(self, **kwargs):
        instance = self.model(**kwargs)

        with transaction.atomic():
            results = self.filter(order=instance.order).aggregate(Max("number"))

            current_number = results["number__max"]
            if current_number is None:
                current_number = 0

            value = current_number + 10
            instance.number = value
            instance.save()

            return instance


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
    end_date = models.DateField(_("end date"), blank=True, null=True,
                                help_text=_("Logo will no longer be visible as of this date, leave empty to display indefinitely"))
    url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="sponsors/logo/")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    @admin.display(description=_("Active"), boolean=True)
    def active(self) -> bool:
        if self.end_date is not None:
            return self.start_date <= timezone.now().date() <= self.end_date

        return self.start_date <= timezone.now().date()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
        ordering = ["name"]

# class Material(models.Model):
#     """A material is an item that is added to an order."""
#
#     class PriceType(models.IntegerChoices):
#         AMOUNT = 0, _("amount")
#         PERCENTAGE = 1, _("percentage")
#
#     description = models.CharField(_("description"), max_length=250, blank=True, null=True)
#     price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)
#     price_type = models.IntegerField(_("price type"), choices=PriceType.choices, default=PriceType.AMOUNT)
#
#     team = models.ForeignKey(
#         Team, on_delete=models.CASCADE, verbose_name=_("team"), blank=True, null=True,
#         help_text=_("Optional. Select a team for which a price should be added.")
#     )
#     role = models.ForeignKey(
#         TeamRole, on_delete=models.CASCADE, verbose_name=_("team role"), blank=True, null=True,
#         help_text=_("Optional. Select a role for which a price should be added.")
#     )
#
#     def __str__(self):
#         return self.description
#
#     def save(self, *args, **kwargs):
#         if self.team and self.role:
#             self.description = "{team} | {team_role}".format(team=self.team.name, team_role=self.role.name)
#
#         elif self.team:
#             self.description = self.team.name
#
#         elif self.role:
#             self.description = self.role.name
#
#         super(Material, self).save(*args, **kwargs)
#
#     class Meta:
#         verbose_name = _("material")
#         verbose_name_plural = _("materials")
#         ordering = ["description"]
#
#     @property
#     def display_price(self) -> str:
#         unit = "&percnt;" if self.price_type == Material.PriceType.PERCENTAGE else settings.CLUB_DEFAULT_CURRENCY_ENTITY
#
#         return mark_safe("{price} {unit}".format(price=self.price, unit=unit))
#
#
# class Order(RulesModel):
#     """Model containing the information related to an order"""
#
#     class OrderStatus(models.IntegerChoices):
#         NEW = 0, _("New")
#         SUBMITTED = 1, _("Submitted")
#         INVOICED = 2, _("Invoiced")
#         PAYED = 3, _("Payed")
#
#     status = models.IntegerField(_("status"), choices=OrderStatus.choices, default=OrderStatus.NEW)
#     season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_("season"))
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False)
#
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return _("Order {uuid}").format(uuid=self.uuid)
#
#     class Meta:
#         verbose_name = _("order")
#         verbose_name_plural = _("orders")
#
#     def total(self) -> Decimal:
#         """Calculates the total for a given order. Each line is processed in order it's added to the order."""
#         total = Decimal(0)
#
#         for line in self.lineitem_set.all().prefetch_related():
#             if line.material.price_type == Material.PriceType.AMOUNT:
#                 total = total + line.material.price
#
#             else:
#                 total = total + (total / 100 * line.material.price)
#
#         return round(total, 2)
#
#     def currency(self) -> str:
#         return mark_safe(settings.CLUB_DEFAULT_CURRENCY_ENTITY)
#
#     def display_total(self) -> str:
#         return mark_safe("{price} {unit}".format(price=self.total(), unit=settings.CLUB_DEFAULT_CURRENCY_ENTITY))
#
#     def members(self) -> list[Member]:
#         members = []
#
#         for item in self.lineitem_set.exclude(member=None).prefetch_related().order_by("member__user__last_name", "member__user__first_name"):
#             if item.member not in members:
#                 members.append(item.member)
#
#         return members
#
#
# class LineItem(RulesModel):
#     """A line item on a given invoice"""
#
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("order"))
#     member = models.ForeignKey(Member, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("member"))
#     material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name=_("item"))
#     number = models.IntegerField(blank=True, null=True)
#
#     objects = LineItemManager()
#
#     def __str__(self):
#         return self.material.description
#
#     def save(self, *args, **kwargs):
#         if self.number is None or self.number == 0:
#             current_max_number = self.order.lineitem_set.aggregate(Max("number"))["number__max"]
#
#             if current_max_number is None:
#                 current_max_number = 0
#
#             self.number = current_max_number + 10
#
#         super(LineItem, self).save(*args, **kwargs)
#
#     class Meta:
#         verbose_name = _("line item")
#         verbose_name_plural = _("line items")
#         ordering = ["number"]
#
#     @property
#     def price(self) -> str:
#         unit = "&percnt;" if self.material.price_type == Material.PriceType.PERCENTAGE else settings.CLUB_DEFAULT_CURRENCY_ENTITY
#
#         return mark_safe("{price} {unit}".format(price=self.material.price, unit=unit))


# auditlog.register(Order)
