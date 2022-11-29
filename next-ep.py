"""
Generates the next episode.
"""
import os
import sys
from pathlib import Path

REVIEW_TEMPLATE = """{% from "reviews/_macros.html" import review_header, review_footer %}

{{ review_header(<num>) }}

{{ review_footer() }}
"""

TABLE_TEMPLATE = """{% extends "tables/classic/_base.html" %}

{% set number = <num> %}
{% set my_rating = raise("unset") %}
{% set skip = "unknown" %}

{% block synopsis %}
Put synopsis here
{% endblock %}
"""

series = sys.argv[1]

templ_dir = Path.cwd() / "templates"
reviews = sorted((templ_dir / "reviews" / series).iterdir(), key=lambda it: int(it.name[2:5]))
first_ep_n = int(reviews[0].name[2:5])
next_ep_n = first_ep_n + len(reviews)
print(f"writing templates for {series} episode {next_ep_n}")

review_f = templ_dir / "reviews" / series / f"ep{next_ep_n:03d}.html"
review_f.write_text(REVIEW_TEMPLATE.replace("<num>", str(next_ep_n)))
os.system(f"git add {review_f}")

table_f = templ_dir / "tables" / series / f"ep{next_ep_n:03d}.html"
table_f.write_text(TABLE_TEMPLATE.replace("<num>", str(next_ep_n)))
os.system(f"git add {table_f}")