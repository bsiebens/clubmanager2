from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def index(request: HttpRequest) -> HttpResponse:
    """The main index page. For now only renders a template, but will be enhanced later on."""

    # TODO also include news items once that app is created/finalized

    welcome_string = _("Good morning")
    if timezone.now().hour > 12 and timezone.now().hour < 18:
        welcome_string = _("Good afternoon")
    elif timezone.now().hour > 18:
        welcome_string = _("Good evening")

    return render(request, "clubmanager/index.html", {"welcome": welcome_string, "site_name": settings.SITE_NAME, "site_logo": settings.SITE_LOGO})


def index_admin(request: HttpRequest) -> HttpResponse:
    """The main admin index page."""

    welcome_string = _("Good morning")
    if timezone.now().hour > 12 and timezone.now().hour < 18:
        welcome_string = _("Good afternoon")
    elif timezone.now().hour > 18:
        welcome_string = _("Good evening")

    return render(
        request, "clubmanager/index_admin.html", {"welcome": welcome_string, "site_name": settings.SITE_NAME, "site_logo": settings.SITE_LOGO}
    )
