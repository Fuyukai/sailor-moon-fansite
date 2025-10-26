"""
Generates the next episode.
"""

import os
import sys
from pathlib import Path

REVIEW_TEMPLATE = """{% extends "_helpers/review.html" %}
{% from "_helpers/images.jinja2" import iimg %}

{% set series_id = "<series>" %}
{% set number = <num> %}

{% block review %}

{% endblock %}
"""

TABLE_TEMPLATE = """{% extends "_helpers/review_table_row.html" %}

{% set number = <num> %}
{% set my_rating = raise("unset") %}
{% set skip = "unknown" %}

{% block synopsis %}
Put synopsis here
{% endblock %}
"""

series = sys.argv[1]

templ_dir = Path.cwd() / "templates"
items = [i for i in (templ_dir / "reviews" / series).iterdir() if i.is_dir()]
reviews = sorted(items, key=lambda it: int(it.name[2:5]))
first_ep_n = int(reviews[0].name[2:5])
next_ep_n = first_ep_n + len(reviews)
print(f"writing templates for {series} episode {next_ep_n}")

ep_dir = templ_dir / "reviews" / series / f"ep{next_ep_n:03d}"
ep_dir.mkdir()

review_f = ep_dir / "index.html"
review_f.write_text(REVIEW_TEMPLATE.replace("<num>", str(next_ep_n)).replace("<series>", series))
os.system(f"git add {review_f}")

table_f = ep_dir / "_table.html"
table_f.write_text(TABLE_TEMPLATE.replace("<num>", str(next_ep_n)))
os.system(f"git add {table_f}")
