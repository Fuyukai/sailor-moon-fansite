"""
A set of Jinja2 related helpers.
"""
from datetime import datetime

from jinja2 import Environment

from makeup import TEMPLATE_DIR


def file_exists(relative_path: str) -> bool:
    """
    Checks if the specified file exists, relative to the template directory.
    """

    return (TEMPLATE_DIR / relative_path).exists()


def raise_helper(msg):
    raise Exception(msg)


def setup_helpers(env: Environment):
    env.globals["file_exists"] = file_exists
    env.globals["raise"] = raise_helper
    env.globals["current_date"] = datetime.utcnow().strftime("%-d %B, %Y, %-I:%M %p")
