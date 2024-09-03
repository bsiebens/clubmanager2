from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def site_name() -> str:
    return settings.SITE_NAME


@register.simple_tag
def site_logo() -> str:
    return settings.SITE_LOGO
