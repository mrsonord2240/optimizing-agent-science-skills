"""Assert that every rendered fix output exists, parses, and contains non-white pixels."""

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
PNGS = [
    *sorted((ROOT / "layouts").glob("*.png")),
    *sorted((ROOT / "r-layouts").glob("*.png")),
    *sorted((ROOT / "static-audit").glob("*.png")),
    ROOT / "edge-bundling.png",
    ROOT / "grn.png",
    ROOT / "cytoscape-demo" / "ppi_network.png",
    ROOT / "cytoscape" / "ppi_network.png",
]

for path in PNGS:
    with Image.open(path) as image:
        rgb = np.asarray(image.convert("RGB"))
        nonwhite = float(np.mean(np.any(rgb < 250, axis=2)))
        assert image.width > 100 and image.height > 100
        assert nonwhite > 0.001
        print(path.relative_to(ROOT), image.size, f"nonwhite={nonwhite:.3f}")

for path in [
    ROOT / "interactive-audit" / "network_basic.html",
    ROOT / "interactive-audit" / "network_styled.html",
]:
    text = path.read_text(encoding="utf-8")
    assert path.stat().st_size > 100_000
    assert "G000" in text and "G099" in text
    print(path.relative_to(ROOT), path.stat().st_size, "bytes; audit node IDs present")

for path in [
    ROOT / "cytoscape-demo" / "ppi_network.pdf",
    ROOT / "cytoscape" / "ppi_network.pdf",
]:
    assert path.read_bytes().startswith(b"%PDF-")
    print(path.relative_to(ROOT), path.stat().st_size, "bytes; PDF header valid")
