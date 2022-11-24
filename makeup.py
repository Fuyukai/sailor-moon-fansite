"""
Makes up the static website.
"""
import shutil
import time
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# set up directories
our_path = Path.cwd()
out_dir = our_path / "out"
shutil.rmtree(out_dir, ignore_errors=True)
out_dir.mkdir()


def raise_helper(msg):
    raise Exception(msg)


before = time.monotonic()
env = Environment(loader=FileSystemLoader(str(our_path / "templates")))
env.globals["raise"] = raise_helper
template = env.get_template("root.html")
data = template.render()

(out_dir / "index.html").write_text(data)
shutil.copytree(our_path / "static", out_dir / "static")

after = time.monotonic()

print(f"built, took {after - before:.04f}s")
