"""
Makes up the static website.
"""

import datetime
import os
import shutil
import time
import zoneinfo
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from makeup import CURRENT_DIR, OUT_DIR, TEMPLATE_DIR
from makeup.helpers import setup_helpers
from makeup.sailor import setup_sailor

# Global Defines ##

#: List of series to process reviews for.
SERIES = [
    "classic",
    "r",
    "s",
    "supers",
    "stars",
]

#: The list of root files, under templates/, to generate output files for.
ROOT_FILES = [
    "index.html",
]

#: The list of directories to recursively scan for .html files to compile.
SCAN_DIRECTORIES = [
    "reviews",
    "content",
]

# Processing code ##
# used to store the number of static files that are included when making up
requested_static_files = [
    (Path("static"), Path("static")),
]


def build_root(env: Environment):
    for file in ROOT_FILES:
        # for files in subdirectories, e.g. `pages/something.html`, make sure the output directory
        # even exists.
        file_output_path = OUT_DIR / file
        file_output_path.parent.mkdir(parents=True, exist_ok=True)
        template = env.get_template(str(file))
        rendered = template.render()

        file_output_path.write_text(rendered)


# build files recursively
def build_recursively(env: Environment):
    for dirname in SCAN_DIRECTORIES:
        dir = Path(dirname)
        path = TEMPLATE_DIR / dir

        for root, _, files in os.walk(path):
            root = Path(root)
            for file in files:
                if os.path.isdir(file):
                    continue

                # skip meta-files, such as macros or templates
                if file.startswith("_"):
                    continue

                full_path = root / file
                inter_path = full_path.relative_to(TEMPLATE_DIR)
                out_path = OUT_DIR / inter_path
                out_path.parent.mkdir(parents=True, exist_ok=True)

                filetime = full_path.stat().st_mtime
                date = datetime.datetime.fromtimestamp(filetime, tz=zoneinfo.ZoneInfo("UTC"))

                if not file.endswith(".html") and not file.endswith(".jinja2"):
                    # file that should be included statically, just directly copy it
                    print(f"copy: {full_path} -> {out_path}")
                    shutil.copy2(full_path, out_path)

                else:
                    print(f"recursively rendering: {full_path!s} -> {out_path}")
                    templ = env.get_template(str(inter_path))
                    rendered = templ.render(file_date=date)
                    out_path.write_text(rendered)


# copy static files
def copy_static_files():
    for input, output in requested_static_files:
        output = OUT_DIR / Path(output)

        if not input.is_absolute():
            input = CURRENT_DIR / input

        output.parent.mkdir(parents=True, exist_ok=True)

        print(f"copy: {input.relative_to(CURRENT_DIR)} -> {output.relative_to(CURRENT_DIR)}")
        if input.is_dir():
            shutil.copytree(input, output)
        else:
            shutil.copy2(input, output)


def main():
    # setup directory code, don't edit this
    OUT_DIR.mkdir(exist_ok=True)

    for f in OUT_DIR.iterdir():
        if f.name == ".git":
            continue

        try:
            shutil.rmtree(f)
        except NotADirectoryError:
            os.remove(f)

    before = time.monotonic()

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    setup_helpers(env)
    setup_sailor(env)

    build_root(env)
    build_recursively(env)
    copy_static_files()

    after = time.monotonic()

    print(f"built, took {after - before:.04f}s")


if __name__ == "__main__":
    main()
