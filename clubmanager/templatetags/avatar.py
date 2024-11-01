#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager
from hashlib import md5
from math import sqrt

from django import template

register = template.Library()


def calculate_brightness(background: dict) -> float:
    """Calculates the brightness of a background image"""
    r_coefficient = 0.241
    g_coefficient = 0.691
    b_coefficient = 0.68

    return sqrt(
        r_coefficient * background["R"] ** 2
        + g_coefficient * background["G"] ** 2
        + b_coefficient * background["B"] ** 2
    )


def foreground(background: dict) -> dict:
    """Calculates the color of the foreground color based on the background"""

    black = {"R": 0, "G": 0, "B": 0}
    white = {"R": 255, "G": 255, "B": 255}

    return black if calculate_brightness(background) > 130 else white


def background(name: str) -> dict:
    """Calculates the background color based on the provided name"""

    name_hash = md5(name.encode("utf-8")).hexdigest()
    name_hash_values = (name_hash[:8], name_hash[8:16], name_hash[16:24])
    background = tuple(int(value, 16) % 256 for value in name_hash_values)

    return {"R": background[0], "G": background[1], "B": background[2]}


@register.inclusion_tag("templatetags/avatar.html")
def avatar(first_name: str, last_name: str, width: int = 12) -> dict:
    full_name = "{first_name} {last_name}".format(
        first_name=first_name, last_name=last_name
    )
    avatar_background = background(full_name)
    avatar_foreground = foreground(avatar_background)

    return {
        "name": "{first_letter}{last_letter}".format(
            first_letter=first_name[0], last_letter=last_name[0]
        ),
        "width": width,
        "background": "#%02x%02x%02x"
        % (avatar_background["R"], avatar_background["G"], avatar_background["B"]),
        "foreground": "#%02x%02x%02x"
        % (avatar_foreground["R"], avatar_foreground["G"], avatar_foreground["B"]),
    }
