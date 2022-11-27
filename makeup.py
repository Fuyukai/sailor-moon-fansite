"""
Makes up the static website.
"""
import os
import shutil
import time
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# global defines
SERIES = [
    "classic",
    "r",
    "s",
    "supers",
    "stars",
]

# set up directories
our_path = Path.cwd()
out_dir = our_path / "out"
shutil.rmtree(out_dir, ignore_errors=True)
out_dir.mkdir()


def raise_helper(msg):
    raise Exception(msg)


templates_dir = our_path / "templates"
tables_dir = templates_dir / "tables"

per_dir: dict[str, list[str]] = {k: [] for k in SERIES}

for d in tables_dir.iterdir():
    if not os.path.isdir(d):
        continue

    for file in d.iterdir():
        if not file.name.startswith("ep"):
            continue

        per_dir[d.name].append(str(file.name))

    # lol
    per_dir[d.name].sort(key=lambda it: int(it[-8:-5]))

before = time.monotonic()
env = Environment(loader=FileSystemLoader(str(templates_dir)))
env.globals["raise"] = raise_helper
env.globals["per_dir"] = per_dir
template = env.get_template("content.html")
data = template.render()

(out_dir / "index.html").write_text(data)

reviews_path = our_path / "templates" / "reviews"
reviews_out = out_dir / "reviews"
reviews_out.mkdir()

for f in reviews_path.iterdir():
    if not f.name.startswith("_") and f.name.endswith(".html"):
        template = env.get_template(f"reviews/{f.name}")
        data = template.render()
        (reviews_out / f.name).write_text(data)

shutil.copytree(our_path / "static", out_dir / "static")

after = time.monotonic()

print(f"built, took {after - before:.04f}s")
