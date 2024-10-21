import uuid

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel

from members.models import Member
from teams.models import Season, Team, TeamRole


class Sponsor(models.Model):
    """A sponsor is displayed on the front page."""

    name = models.CharField(_("name"), max_length=250)
    start_date = models.DateField(_("start date"), default=timezone.now, help_text=_("Logo will be visible as of this day"))
    end_date = models.DateField(_("end date"), blank=True, null=True, help_text=_("Logo will no longer be visible as of this date, leave empty to display indefinitly"))
    url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="sponsors/logo/")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    @admin.display(description=_("Active"), boolean=True)
    def active(self) -> bool:
        if self.end_date is not None:
            return self.start_date <= timezone.now().date() and timezone.now().date() <= self.end_date

        return self.start_date <= timezone.now().date()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
        ordering = ["name"]


class Invoice(RulesModel):
    """Model containing the information related to subscriptions"""

    class InvoiceStatus(models.IntegerChoices):
        NEW = 0, _("New")
        SUBMITTED = 1, _("Submitted")
        INVOICED = 2, _("Invoiced")
        PAYED = 3, _("Payed")

    status = models.IntegerField(_("status"), choices=InvoiceStatus.choices, default=InvoiceStatus.NEW)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_("season"))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return _("Invoice {uuid}").format(uuid=self.uuid)

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")


class Material(models.Model):
    """A material is an item that is added to an invoice."""

    class PriceType(models.IntegerChoices):
        AMOUNT = 0, _("amount")
        PERCENTAGE = 1, _("percentage")

    description = models.CharField(_("description"), max_length=250, blank=True, null=True)
    price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)
    price_type = models.IntegerField(_("price type"), choices=PriceType.choices, default=PriceType.AMOUNT)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("team"), blank=True, null=True)
    role = models.ForeignKey(TeamRole, on_delete=models.CASCADE, verbose_name=_("team role"), blank=True, null=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.team is not None or self.role is not None:
            if self.team is not None and self.role is not None:
                self.description = "{team} | {team_role}".format(team=self.team.name, team_role=self.role.name)

            else:
                if self.team is not None:
                    self.description = self.team.name
                else:
                    self.description = self.role.name

        super(Material, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("material")
        verbose_name_plural = _("materials")


class LineItem(RulesModel):
    """A line item on a given invoice"""

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name=_("invoice"))
    member = models.ForeignKey(Member, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("member"))
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name=_("item"))

    def __str__(self):
        return self.material.description

    class Meta:
        verbose_name = _("line item")
        verbose_name_plural = _("line items")
