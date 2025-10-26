"""
Sailor-specific extensions.
"""

from jinja2 import Environment

from makeup import TEMPLATE_DIR

REVIEWS_DIR = TEMPLATE_DIR / "reviews"


def title_to_id(series: str) -> str:
    lower = series.lower()

    if lower == "sailor stars":
        return "stars"

    if lower == "r":
        return "romance"

    if lower == "s":
        return "super"

    return lower


def id_to_title(id: str) -> str:
    if id == "romance":
        return "R"

    if id == "super":
        return "S"

    if id == "supers":
        return "SuperS"

    if id == "stars":
        return "Sailor Stars"

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
        
        case _:
            raise ValueError(f"Unknown series: {series}")


def relative_number(number: int) -> int:
    """
    Gets the season-relative number, as opposed to the absolute number.
    """

    if 0 < number <= 46:
        return number

    if 46 < number <= 90:
        return number - 46

    if 90 < number <= 127:
        return number - 90

    if 127 < number <= 165:
        return number - 127

    if number <= 200:
        return number - 165

    raise ValueError(f"invalid episode number: {number}")


def id_for_ep(number: int) -> str:
    if 0 < number <= 46:
        return "classic"

    if 46 < number <= 90:
        return "romance"

    if 90 < number <= 127:
        return "super"

    if 127 < number <= 165:
        return "supers"

    if number <= 200:
        return "stars"

    raise ValueError(f"invalid episode number: {number}")


def setup_sailor(env: Environment):
    env.globals["title_to_id"] = title_to_id
    env.globals["id_to_title"] = id_to_title
    env.globals["id_for_ep"] = id_for_ep
    env.globals["episode_ranges"] = episode_ranges
    env.globals["relative_number"] = relative_number
