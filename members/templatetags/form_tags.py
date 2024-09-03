from typing import Any
from django import template
from django.forms import BoundField

register = template.Library()


@register.inclusion_tag("templatetags/field.html")
def form_field(
    field: BoundField,
    label: str | None = None,
    help_text: str | None = None,
    show_label: bool = True,
    show_help: bool = True,
    show_placeholder: bool = True,
    size: str = "full",
) -> dict[str, Any]:
    """Creates HTML output for a field"""
    if label is not None:
        field.label = label

    if help_text is not None:
        field.help_text = help_text

    field_type = None
    match field.widget_type:
        case "select" | "nullbooleanselect" | "radioselect":
            field_type = "select"
        case "checkbox":
            field_type = "checkbox"
        case "textarea" | "markdownx":
            field_type = "textarea"
        case "clearablefile":
            field_type = "file"
        case "selectmultiple":
            field_type = "select"
        case _:
            field_type = "input"

    size_modifier = None
    match size:
        case "extra-small":
            size_modifier = "xs"
        case "small":
            size_modifier = "sm"
        case _:
            pass

    return {"field": field, "show_label": show_label, "show_help": show_help, "show_placeholder": show_placeholder, "field_type": field_type, "size_modifier": size_modifier}


@register.inclusion_tag("templatetags/display_field.html")
def display_field(
    field: BoundField,
    alternate_label: str | None = None,
    display_label: bool = True,
    display_placeholder: bool = True,
    display_size: str = "default",
    display_helptext: bool = True,
    alternate_helptext: str | None = None,
    small: bool = False,
):
    """
    Print HTML for a field.
    Optionally, a label can be supplied that overrides the default label generated for the form.

    Example:
    {% display_field form.my_field "My New Label" %}
    """
    if alternate_label is not None:
        field.label = alternate_label

    if alternate_helptext is not None:
        field.help_text = alternate_helptext

    input_classes = ""
    width_classes = "w-full lg:w-fit"
    match display_size:
        case "xs":
            match field.widget_type:
                case "clearablefile":
                    input_classes = "file-input-xs"
                case "checkbox":
                    input_classes = "checkbox-xs"
                case "select":
                    input_classes = "select-xs"
                case _:
                    input_classes = "input-xs"

        case "sm":
            match field.widget_type:
                case "clearablefile":
                    input_classes = "file-input-sm"
                case "checkbox":
                    input_classes = "checkbox-sm"
                case "select":
                    input_classes = "select-sm"
                case _:
                    input_classes = "input-sm"

        case "full":
            width_classes = "w-full"

        case _:
            input_classes = ""

    return {
        "field": field,
        "type": field.widget_type,
        "display_label": display_label,
        "display_placeholder": display_placeholder,
        "display_helptext": display_helptext,
        "input_classes": input_classes,
        "width_classes": width_classes,
        "small": small,
    }
