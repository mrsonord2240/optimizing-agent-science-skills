"""Parse shipped sources and measure every rendered PNG/PDF audit artifact."""
from __future__ import annotations

import ast
from pathlib import Path
import sys

from PIL import Image


if len(sys.argv) != 3:
    raise SystemExit("usage: verify_artifacts.py <skill-copy> <out-dir>")
skill = Path(sys.argv[1])
out = Path(sys.argv[2])

for path in sorted(skill.rglob("*.py")):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print("PY_PARSE PASS", path.relative_to(skill))

pngs = sorted(out.glob("*.png"))
if len(pngs) < 8:
    raise AssertionError(f"expected at least 8 PNGs, got {len(pngs)}")
for path in pngs:
    im = Image.open(path).convert("RGB")
    pixels = list(im.getdata())
    nonwhite = sum(p != (255, 255, 255) for p in pixels) / len(pixels)
    print("PNG", path.name, "bytes", path.stat().st_size, "pixels", im.size, "nonwhite", round(nonwhite, 5))
    assert path.stat().st_size > 1_000 and min(im.size) >= 300 and nonwhite > 0.005

pdfs = sorted(out.glob("*.pdf"))
for path in pdfs:
    print("PDF", path.name, "bytes", path.stat().st_size)
    assert path.stat().st_size > 1_000

print("ARTIFACT VERIFICATION PASS", len(pngs), "PNGs", len(pdfs), "PDFs")
