"""Build a labeled contact sheet from every rendered PNG audit artifact."""

from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


if len(sys.argv) != 2:
    raise SystemExit("usage: make_contact_sheet.py <out-dir>")

out = Path(sys.argv[1])
paths = sorted(path for path in out.glob("*.png") if path.name != "contact_sheet.png")
if not paths:
    raise RuntimeError("no PNG artifacts found")

columns = 4
tile_width, tile_height = 480, 330
label_height = 30
rows = (len(paths) + columns - 1) // columns
sheet = Image.new("RGB", (columns * tile_width, rows * (tile_height + label_height)), "white")
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default(size=16)

for index, path in enumerate(paths):
    image = Image.open(path).convert("RGB")
    image.thumbnail((tile_width - 12, tile_height - 12))
    column = index % columns
    row = index // columns
    x = column * tile_width + (tile_width - image.width) // 2
    y = row * (tile_height + label_height) + label_height + (tile_height - image.height) // 2
    sheet.paste(image, (x, y))
    draw.text(
        (column * tile_width + 8, row * (tile_height + label_height) + 6),
        path.name,
        fill="black",
        font=font,
    )

target = out / "contact_sheet.png"
sheet.save(target)
print(target, sheet.size, len(paths), "artifacts")
