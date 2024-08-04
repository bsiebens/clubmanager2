from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .signals import new_member_user_created


class UserManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("user")


class Member(models.Model):
    """User profile for a given member."""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_("user"))
    notes = models.TextField(_("notes"), blank=True)

    birth_date = models.DateField(_("birth date"), blank=True, null=True)
    license = models.CharField(_("license"), blank=True, null=True, max_length=250)

    phone = PhoneNumberField(verbose_name=_("phone"), blank=True, null=True)
    emergency_phone_primary = PhoneNumberField(verbose_name=_("first emergency phone"))
    emergency_phone_secondary = PhoneNumberField(verbose_name=_("second emergency phone"), blank=True, null=True)

    password_change_required = models.BooleanField(
        _("password change needed"),
        default=False,
        help_text=_("If flagged signals that this users will need to reset their password at the next login."),
    )

    is_organization_admin = models.BooleanField(
        _("Organization admin"), default=False, help_text=_("An organization admin will have advanced access rights into the system.")
    )

    objects = UserManager()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def first_name(self) -> str:
        return self.user.first_name

    @property
    def last_name(self) -> str:
        return self.user.last_name

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def email(self) -> str:
        return self.user.email

    def get_full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")
        ordering = ["user__last_name", "user__first_name", "user__username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    @classmethod
    def create_member(cls, first_name: str, last_name: str, email: str, username: str, password: str | None = None) -> "Member":
        """Creates a new member and user."""

        member = cls()
        users = get_user_model().objects.filter(first_name=first_name, last_name=last_name, email=email, username=username)
        send_signal = False

        if users.count() == 1:
            member.user = users.first()

        else:
            user = get_user_model().objects.create(first_name=first_name, last_name=last_name, email=email, username=username, is_active=True)
            member.user = user
            send_signal = True

        member.save()

        if send_signal:
            new_member_user_created.send(member, password=password)

        return member


class Family(models.Model):
    """A family is a collection of members that belong together. A member can be a part of multiple families, within a family all information is shared."""

    name = models.CharField(_("name"), max_length=250)
    members = models.ManyToManyField(Member, verbose_name=_("members"))

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("family")
        verbose_name_plural = _("families")


# Log both models into the audit log to maintain track of changes and who made them.
auditlog.register(Member)
auditlog.register(Family)
