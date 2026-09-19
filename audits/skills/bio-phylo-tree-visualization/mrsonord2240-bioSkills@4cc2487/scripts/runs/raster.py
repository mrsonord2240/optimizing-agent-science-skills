"""Auditor helper: rasterize PDF/SVG figures to PNG so they can be visually inspected (not part of the Skill)."""
import sys, pathlib
import fitz  # pymupdf

for p in sys.argv[1:]:
    p = pathlib.Path(p)
    doc = fitz.open(str(p))
    page = doc[0]
    zoom = float(__import__('os').environ.get('ZOOM', '1.5'))
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    out = p.with_name(p.stem + '_' + p.suffix.lstrip('.') + '_view.png')
    pix.save(str(out))
    print(out, pix.width, 'x', pix.height, 'page pts', round(page.rect.width), 'x', round(page.rect.height))
