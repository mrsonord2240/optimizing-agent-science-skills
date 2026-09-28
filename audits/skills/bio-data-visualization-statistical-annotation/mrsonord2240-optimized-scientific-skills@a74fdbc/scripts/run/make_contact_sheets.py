"""Assemble generated figures into readable contact sheets for visual inspection."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "run" / "output"
FIGS = ROOT / "figs"
FIGS.mkdir(parents=True, exist_ok=True)


def make_sheet(paths: list[Path], destination: Path, columns: int = 3) -> None:
    thumb_w, thumb_h, label_h = 520, 440, 40
    rows = (len(paths) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=18)
    for index, path in enumerate(paths):
        row, column = divmod(index, columns)
        with Image.open(path) as opened:
            image = opened.convert("RGB")
        image.thumbnail((thumb_w - 16, thumb_h - 16), Image.Resampling.LANCZOS)
        x = column * thumb_w + (thumb_w - image.width) // 2
        y = row * (thumb_h + label_h) + (thumb_h - image.height) // 2
        canvas.paste(image, (x, y))
        label = str(path.relative_to(OUTPUT)).replace("\\", "/")
        draw.text((column * thumb_w + 8, row * (thumb_h + label_h) + thumb_h + 6), label, fill="black", font=font)
    canvas.save(destination)


regression = sorted(path for path in OUTPUT.glob("*.png") if "welch" not in path.name)
new_and_example = [OUTPUT / "py_welch_unequal_variance.png"] + sorted((OUTPUT / "example").glob("*.png"))
make_sheet(regression, FIGS / "regression_plots_contact.png")
make_sheet(new_and_example, FIGS / "new_and_example_plots_contact.png")
print(FIGS / "regression_plots_contact.png")
print(FIGS / "new_and_example_plots_contact.png")
