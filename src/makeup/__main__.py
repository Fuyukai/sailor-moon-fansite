"""
Makes up the static website.
"""

import datetime
import os
import shutil
import time
from functools import partial
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# setup directory code, don't edit this
CURRENT_DIR = Path.cwd()
OUT_DIR = CURRENT_DIR / "out"
TEMPLATE_DIR = CURRENT_DIR / "templates"

OUT_DIR.mkdir(exist_ok=True)

for f in OUT_DIR.iterdir():
    try:
        shutil.rmtree(f)
    except NotADirectoryError:
        os.remove(f)

## Global Defines ##

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
    "watch_guide.html"
]

#: The list of directories to recursively scan for .html files to compile.
SCAN_DIRECTORIES = [
    "reviews"
]

## Processing code ##
# used to store the number of static files that are included when making up
requested_static_files = [
    (Path("static"), Path("static")),
]


def raise_helper(msg):
    raise Exception(msg)


# noinspection PyShadowingNames
def include_static_helper(relative_dir, path: str):
    """
    Includes a static file or directory in the built output. This is relative to the compiled
    template (which is defined statically, not dynamically)'s relative parent directory

    If you need to include files globally, put them in the ``/static`` directory.

    This function returns the relativised filename, to allow doing things like e.g.
    ``<img src="{{ include_static("screenshot.png") }}>``.
    """

    web_path = relative_dir / path
    real_path = TEMPLATE_DIR / web_path

    requested_static_files.append((real_path, web_path))
    return requested_static_files


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
                # skip meta-files, such as macros or templates
                if file.startswith("_"):
                    continue

                full_path = root / file
                inter_path = full_path.relative_to(TEMPLATE_DIR)
                out_path = OUT_DIR / inter_path
                out_path.parent.mkdir(parents=True, exist_ok=True)

                # create inclusion helper
                fn = partial(include_static_helper, inter_path.parent)

                print(f"recursively rendering: {str(full_path)} -> {out_path}")
                templ = env.get_template(str(inter_path))
                rendered = templ.render(include_static=fn)
                out_path.write_text(rendered)


# copy static files
def copy_static_files():
    for input, output in requested_static_files:
        output = OUT_DIR / Path(output)

        if not input.is_absolute():
            input = CURRENT_DIR / input

        print(f"copy: {input.relative_to(CURRENT_DIR)} -> {output.relative_to(CURRENT_DIR)}")
        if input.is_dir():
            pass
            shutil.copytree(input, output)
        else:
            pass
            shutil.copy2(input, output)


def main():
    before = time.monotonic()

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    env.globals["raise"] = raise_helper
    env.globals["current_date"] = datetime.datetime.utcnow().strftime("%-d %B, %Y, %-I:%M %p")

    build_root(env)
    build_recursively(env)
    copy_static_files()

    after = time.monotonic()

    print(f"built, took {after - before:.04f}s")


main()
