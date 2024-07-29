from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .signals import new_member_user_created


class Member(models.Model):
    """User profile for a given member."""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_("user"))
    notes = models.TextField(_("notes"), blank=True)

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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    @classmethod
    def create_member(cls, first_name: str, last_name: str, email: str, username: str) -> "Member":
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
            new_member_user_created.send(member)

        return member


class Family(models.Model): ...
