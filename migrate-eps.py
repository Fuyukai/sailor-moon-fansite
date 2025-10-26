import shutil

from makeup import CURRENT_DIR, TEMPLATE_DIR

table_dir = TEMPLATE_DIR / "tables"
tables = TEMPLATE_DIR / "tables" / "classic"
reviews = TEMPLATE_DIR / "reviews" / "classic"

for i in tables.iterdir():
    if i.name == "_base.html":
        continue

    new_path = reviews / i.with_suffix("").name
    if new_path.name == "ep001":
        continue

    new_path.mkdir(exist_ok=True, parents=True)
    table_data = i.read_text()
    table_data = table_data.replace(
        '{% extends "tables/classic/_base.html" %}',
        '{% extends "_helpers/review_table_row.html" %}',
    )
    # copy over _table
    (new_path / "_table.html").write_text(table_data)

    # read in and fixup review code
    review_file = new_path.with_suffix(".html")

    # awful, awful replaceement
    content = review_file.read_text(encoding="utf-8")
    new = content.replace(
        '{% from "reviews/_macros.html" import review_header, review_footer %}',
        '{% extends "_helpers/review.html" %}',
    )
    new = new.replace("{{ review_header(", '{% set series_id = "classic" %}\n{% set number = ')
    new = new.replace(") }}\n<", " %}\n\n{% block review %}\n<")
    new = new.replace("{{ review_footer() }}", "{% endblock %}")

    review_out = new_path / "index.html"
    review_out.write_text(new)

    # finally, copy the images
    image = CURRENT_DIR / "static/screenshots/classic" / i.with_suffix(".jpg").name
    if not image.exists():
        print("skipping", image.name)
        continue

    image_out = new_path / "preview.jpg"
    shutil.copy(image, image_out)
