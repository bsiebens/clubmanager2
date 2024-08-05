from django import template
from django.forms import BoundField

register = template.Library()


@register.inclusion_tag("templatetags/display_field.html")
def display_field(
    field: BoundField,
    alternate_label: str | None = None,
    display_label: bool = True,
    display_placeholder: bool = True,
    display_size: str = "default",
):
    """
    Print HTML for a field.
    Optionally, a label can be supplied that overrides the default label generated for the form.

    Example:
    {% display_field form.my_field "My New Label" %}
    """
    if alternate_label is not None:
        field.label = alternate_label

    input_classes = ""
    match display_size:
        case "xs":
            input_classes = "input-xs"
        case _:
            input_classes = ""

    return {
        "field": field,
        "type": field.widget_type,
        "display_label": display_label,
        "display_placeholder": display_placeholder,
        "input_classes": input_classes,
    }
