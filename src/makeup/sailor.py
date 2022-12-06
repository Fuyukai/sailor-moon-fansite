"""
Sailor-specific extensions.
"""

from makeup import CURRENT_DIR, TEMPLATE_DIR, OUT_DIR
from jinja2 import Environment

REVIEWS_DIR = TEMPLATE_DIR / "reviews"


def title_to_id(series: str) -> str:
    lower = series.lower()

    if lower == "sailor stars":
        return "stars"

    elif lower == "r":
        return "romance"

    elif lower == "s":
        return "super"

    return lower


def id_to_title(id: str) -> str:
    if id == "romance":
        return "R"

    elif id == "super":
        return "S"

    elif id == "supers":
        return "SuperS"

    elif id == "stars":
        return "Sailor Stars"

    else:
        return id.title()


def episode_ranges(series: str) -> range:
    """
    Gets the episode ranges for the specified series.
    """

    # stupid exclusive ranges
    match series.lower():
        case "classic":
            return range(1, 47)

        case "romance":
            return range(47, 90)

        case "super":
            return range(90, 128)

        case "supers":
            return range(128, 166)

        case "stars":
            return range(166, 200)

    raise ValueError(f"Unknown series: {series}")


def id_for_ep(number: int) -> str:
    if 0 < number <= 46:
        return "classic"

    elif 46 < number <= 90:
        return "romance"

    elif 90 < number <= 127:
        return "super"

    elif 127 < number <= 165:
        return "supers"

    elif number <= 200:
        return "stars"

    raise ValueError(f"invalid episode number: {number}")


def setup_sailor(env: Environment):
    env.globals["title_to_id"] = title_to_id
    env.globals["id_to_title"] = id_to_title
    env.globals["id_for_ep"] = id_for_ep
    env.globals["episode_ranges"] = episode_ranges
