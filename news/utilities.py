import re
from typing import Optional

from django.db.models import QuerySet
from django.template.defaultfilters import slugify


def unique_slugify(instance: any, value: str, slug_field_name: str = "slug", queryset: Optional[QuerySet] = None, slug_separator: str = "-") -> None:
    """Calculates a unique slug of ``value`` for an instance.

    Arguments:
        ``instance`` - object to work on
        ``value`` - string that will be used as input to derive the slug from
        ``slug_field_name`` - field on object to store the derived slug
        ``queryset`` - usually doesn't need to be set explicitely, will default to ``.all()`` queryset from model's default manager
        ``slug_separator`` - string used to split slug parts

    Returns:
        Object with the ``slug_field_name`` attribute updated to the unique slug"""
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = "%s%s" % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[: slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = "%s%s" % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value: str, separator: str = "-") -> str:
    """Cleans up a slug by removing slug separator characters that occur at the beginning or end of a slug.
    If an alternate separator is used, it will also replace any instance of the default "-" separator with the new separator."""
    separator = separator or ""
    if separator == "-" or not separator:
        re_sep = "-"
    else:
        re_sep = "(?:-|%s)" % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub("%s+" % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != "-":
            re_sep = re.escape(separator)
        value = re.sub(r"^%s+|%s+$" % (re_sep, re_sep), "", value)
    return value
