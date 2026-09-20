#!/usr/bin/env python3
"""Render page 1 of a PDF to PNG and print its extractable text. Needs pymupdf (installed with pip --target into audits/bio-sashimi-plots/_pkgs, not in any shared env)."""
import sys
sys.path.insert(0, 'F:/OpenScience/audits/bio-sashimi-plots/_pkgs')
import fitz
pdf, png = sys.argv[1], sys.argv[2]
d = fitz.open(pdf)
p = d[0]
print('pages', len(d), 'page size pt', p.rect.width, p.rect.height)
p.get_pixmap(dpi=int(sys.argv[3]) if len(sys.argv) > 3 else 80).save(png)
print('TEXT:', ' | '.join(t for t in p.get_text().split('\n') if t.strip()))
