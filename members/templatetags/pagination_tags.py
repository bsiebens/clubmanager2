from django import template
from urllib.parse import urlencode

from django.http import HttpRequest, QueryDict

register = template.Library()


@register.simple_tag
def url_replace(request: HttpRequest, field: str, value: str | int, default_field: str | None = None, default_value: str | int | None = None) -> str:
    """Updates the given field in the GET parameters with the supplied value. If field does not exist, it is added."""
    dict_ = request.GET.copy()
    dict_[field] = value

    if default_field is not None and default_field not in dict_.keys():
        dict_[default_field] = default_value

    return dict_.urlencode()
