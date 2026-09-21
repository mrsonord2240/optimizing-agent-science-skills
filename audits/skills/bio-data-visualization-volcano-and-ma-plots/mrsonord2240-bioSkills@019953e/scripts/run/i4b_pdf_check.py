# Input 4 follow-up: inspect PDFs written by the shipped example (page size, embedded fonts).
import re, pathlib
D = pathlib.Path(r"F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\run\scratch4")
for tag in ("ensembl", "symbols"):
    for f in ("volcano.pdf", "ma_plot.pdf"):
        b = (D / tag / f).read_bytes()
        mb = re.search(rb"/MediaBox\s*\[([^\]]*)\]", b)
        w, h = [float(x) for x in mb.group(1).split()[2:4]] if mb else (0, 0)
        print(f"{tag}/{f}: {len(b)} bytes; page {w:.1f}x{h:.1f} pt = {w/72*25.4:.1f}x{h/72*25.4:.1f} mm; /TrueType={b.count(b'/TrueType')} /CIDFontType2={b.count(b'/CIDFontType2')} /Type3={b.count(b'/Type3')} /FontFile2={b.count(b'/FontFile2')}")
