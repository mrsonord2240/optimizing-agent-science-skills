"""Parse every generated raster/PDF/HTML and emit independent artifact metrics."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
results: dict[str, dict[str, object]] = {}
for path in sorted(OUT.rglob("*")):
    if not path.is_file():
        continue
    relative = str(path.relative_to(ROOT))
    if path.suffix.lower() == ".png":
        image = Image.open(path).convert("RGB")
        array = np.asarray(image)
        nonwhite = float(np.mean(np.any(array < 250, axis=2)))
        results[relative] = {
            "kind": "png",
            "bytes": path.stat().st_size,
            "width": image.width,
            "height": image.height,
            "nonwhite": round(nonwhite, 6),
        }
        assert image.width > 100 and image.height > 100
        assert path.stat().st_size > 2000 and nonwhite > 0.001
    elif path.suffix.lower() == ".pdf":
        header = path.read_bytes()[:5]
        results[relative] = {
            "kind": "pdf",
            "bytes": path.stat().st_size,
            "header": header.decode("ascii", errors="replace"),
        }
        assert header == b"%PDF-" and path.stat().st_size > 1000
    elif path.suffix.lower() == ".html":
        text = path.read_text(encoding="utf-8")
        results[relative] = {
            "kind": "html",
            "bytes": path.stat().st_size,
            "vis_network": "vis-network" in text,
        }
        assert path.stat().st_size > 100_000 and "vis-network" in text
(ROOT / "logs/artifact_metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print("validated", len(results), "artifacts")
print(json.dumps(results, indent=2))
