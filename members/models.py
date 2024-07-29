from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Member(models.Model):
    """User profile for a given member."""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_("user"))


class Family(models.Model): ...
