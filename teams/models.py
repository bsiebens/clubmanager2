import datetime

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from members.models import Member


def team_season_path(instance: "TeamPicture", filename: str) -> str:
    return "groups/picture/{instance.team.slug}/{instance.season.start_year}/{filename}".format(instance=instance, filename=filename)


class Season(models.Model):
    """A season of play"""

    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"))

    def __str__(self):
        return _("Season '{start} - '{end}").format(start=self.start_date.strftime("%y"), end=self.end_date.strftime("%y"))

    class Meta:
        verbose_name = _("season")
        verbose_name_plural = _("seasons")
        ordering = ["start_date"]

    @classmethod
    def get_season(cls, date: datetime.date = timezone.now(), return_values_only: bool = False) -> "list | Season":
        """
        Returns the season for the given date.

        * `date` date to check, default = `timezone.now()`
        * `return_values_only` if true, will only return start and end date, no object, default = `False`

        Raises `DoesNotExist` if no Season exists.
        """
        season = cls.objects.get(start_date__lte=date, end_date__gte=date)

        if return_values_only:
            return [season.start_date, season.end_date]
        return season

    @classmethod
    def get_season_id(cls, date: datetime.date = timezone.now()) -> int:
        season = Season.get_season(date=date, return_values_only=False)
        return season.id

    @property
    @admin.display(description=_("Current Season"), boolean=True)
    def current_season(self):
        return self == Season.get_season()

    @property
    def start_year(self) -> int:
        return self.start_date.strftime("%Y")

    def has_started(self) -> bool:
        return self.start_date < timezone.now().date()


class NumberPool(models.Model):
    """A number pool holds all numbers that can be assigned, within a pool you can enforce unique numbers."""

    name = models.CharField(_("name"), max_length=250, unique=True)
    enforce_unique = models.BooleanField(_("enforce unique"), default=True, help_text=_("If selected will enforce unique numbers on all players"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("number pool")
        verbose_name_plural = _("number pools")


class TeamRole(models.Model):
    """Roles that can be assigned to team members"""

    name = models.CharField(_("name"), max_length=250, unique=True)
    abbreviation = models.CharField(_("abbreviation"), max_length=10, help_text=_("Abbreviated version of the name"), unique=True)
    staff_role = models.BooleanField(_("staff"), default=False, help_text=_("Staff roles are displayed on the team page under the staff section"))
    admin_role = models.BooleanField(_("admin"), default=False, help_text=_("Admin roles can manage the team (add/remove members, post messages, create events)"))
    sort_order = models.IntegerField(
        _("sort order"),
        default=100,
        help_text=_(
            "By adjusting the sort order this role will displayed higher on the team page, by default roles are sorted by order (low to high) and then alphabetically"
        ),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("team role")
        verbose_name_plural = _("team roles")
        ordering = ["sort_order", "name"]


class Team(models.Model):
    """A team"""

    class TeamTypes(models.TextChoices):
        INTERNAL = "INT", _("Internal")
        EXTERNAL = "EXT", _("External")

    name = models.CharField(_("name"), max_length=250)
    short_name = models.CharField(_("short name"), max_length=250, help_text=_("An optional short name"), blank=True, null=True)
    slug = AutoSlugField(populate_from=["name"], verbose_name=_("slug"), editable=True, overwrite_on_add=False)
    type = models.CharField(
        _("type"),
        max_length=3,
        choices=TeamTypes.choices,
        default=TeamTypes.INTERNAL,
        help_text=_("Internal groups are only visible to members, external groups are available via the API"),
    )
    number_pool = models.ForeignKey(NumberPool, on_delete=models.PROTECT, verbose_name=_("number pool"), to_field="name", default="default")

    members = models.ManyToManyField(Member, verbose_name=_("members"), through="TeamMembership")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    @property
    def get_short_name(self) -> str:
        """Returns short_name if exists, otherwise falls back to name"""
        if self.short_name is not None and self.short_name != "":
            return self.short_name

        return self.name


class TeamMembership(models.Model):
    """Linking members to teams"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("team"))
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name=_("member"))
    season = models.ForeignKey(Season, on_delete=models.PROTECT, verbose_name=_("season"))
    role = models.ForeignKey(TeamRole, on_delete=models.PROTECT, verbose_name=_("role"))

    number = models.IntegerField(_("number"), blank=True, null=True)
    captain = models.BooleanField(_("captain"), default=False, help_text=_("Mark as team captain"))
    assistant_captain = models.BooleanField(_("assistant captain"), default=False, help_text=_("Mark as assistant team captain"))

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return _("{team} - {member}").format(team=self.team, member=self.member)

    class Meta:
        verbose_name = _("team membership")
        verbose_name_plural = _("team memberships")
        ordering = ["team__name", "role__sort_order", "number", "member__user__last_name", "member__user__first_name"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(number__gte=0) | models.Q(number__lte=99),
                name="number_0-99",
                violation_error_message=_("Number must be between 0 and 99"),
            ),
            models.UniqueConstraint(
                fields=["team", "season", "number"],
                name="team_season_number_unique",
                violation_error_message=_("Number already in use for this team in the current season"),
            ),
        ]

    def clean(self) -> None:
        if self.number is not None and self.team.number_pool.enforce_unique:
            base_query = TeamMembership.objects.filter(number=self.number, team__number_pool=self.team.number_pool)

            if self.id is not None:
                base_query = base_query.exclude(pk=self.id)

            if base_query.count() > 0:
                raise ValidationError(_("Number already in use, please update to a unique number."))

        return super(TeamMembership, self).clean()


class TeamPicture(models.Model):
    """A picture for a given team in a given season"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("team"))
    season = models.ForeignKey(Season, on_delete=models.PROTECT, verbose_name=_("season"))
    picture = models.ImageField(_("picture"), upload_to=team_season_path)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.picture.name

    class Meta:
        verbose_name = _("team picture")
        verbose_name_plural = _("team pictures")
