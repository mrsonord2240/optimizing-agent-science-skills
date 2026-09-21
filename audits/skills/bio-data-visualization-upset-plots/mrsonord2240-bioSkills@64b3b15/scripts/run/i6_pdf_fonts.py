"""Usage-guide step 8 claims 'Type-42 fonts (Python)' and 'cairo_pdf (R)'. Check the PDFs actually produced by the Skill's own code."""
import re, zlib, sys
def fonts(path):
    b = open(path, 'rb').read(); txt = b.decode('latin-1')
    for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', b, re.S):
        try: txt += zlib.decompress(m.group(1)).decode('latin-1')
        except Exception: pass
    return {k: len(re.findall(k, txt)) for k in ['/Type3', '/TrueType', '/CIDFontType2', '/Subtype */Type1', '/Type1C', '/FontFile2', '/BaseFont']}, sorted(set(re.findall(r'/BaseFont\s*/([A-Za-z0-9+\-]+)', txt)))
for p in ['F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/ex_R/upset_basic.pdf', 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/i3a_skill_block.pdf']:
    print(p.split('/')[-1], fonts(p))
import matplotlib; print('matplotlib default pdf.fonttype =', matplotlib.rcParams['pdf.fonttype'])
import subprocess
