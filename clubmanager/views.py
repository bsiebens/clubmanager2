from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rules.contrib.views import PermissionRequiredMixin


class MessagesDeniedMixin(PermissionRequiredMixin):
    """An updated version of the PermissionRequiredMixin class that sets the denied message in the messages queue and redirects to a given page."""

    permission_denied_message = _("You do not have access to the requested page")
    redirect_to = reverse_lazy("clubmanager_admin:index")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())

        return HttpResponseRedirect(redirect_to=self.redirect_to)


def index(request: HttpRequest) -> HttpResponse:
    """The main index page. For now only renders a template, but will be enhanced later on."""

    # TODO also include news items once that app is created/finalized

    welcome_string = _("Good morning")
    if 12 < timezone.now().hour < 18:
        welcome_string = _("Good afternoon")
    elif timezone.now().hour > 18:
        welcome_string = _("Good evening")

    return render(request, "clubmanager/index.html", {"welcome": welcome_string, "site_name": settings.SITE_NAME, "site_logo": settings.SITE_LOGO})


@login_required
@permission_required("teams")
def index_admin(request: HttpRequest) -> HttpResponse:
    """The main admin index page."""

    welcome_string = _("Good morning")
    if 12 < timezone.now().hour < 18:
        welcome_string = _("Good afternoon")
    elif timezone.now().hour > 18:
        welcome_string = _("Good evening")

    return render(request, "clubmanager/index_admin.html",
                  {"welcome": welcome_string, "site_name": settings.SITE_NAME, "site_logo": settings.SITE_LOGO})
