# Input 5: inspect raincloud.pdf written by the shipped example (ggsave width=89 height=70 units=mm device=cairo_pdf), ggplot2 3.5.2 run; and the failed ggplot2 4.0.3 leftover
import re, zlib
base = r"F:\OpenScience\audits\bio-data-visualization-distribution-plots\run\out\i5" + "\\"
def inflate_all(b):
    out = [b]
    for m in re.finditer(rb"stream\r?\n", b):
        s = m.end(); e = b.find(b"endstream", s)
        try: out.append(zlib.decompress(b[s:e]))
        except Exception: pass
    return b"\n".join(out)
for name in ["raincloud.pdf", "raincloud_gg4_FAILED.pdf"]:
    b = open(base + name, "rb").read(); t = inflate_all(b)
    print("==", name, "bytes", len(b))
    m = re.search(rb"/MediaBox\s*\[([^\]]*)\]", t)
    print("MediaBox", m.group(1).decode() if m else None)
    if m:
        v = [float(x) for x in m.group(1).split()]
        w, h = (v[2]-v[0])*25.4/72, (v[3]-v[1])*25.4/72
        print("page mm: %.2f x %.2f" % (w, h), "PASS" if abs(w-89) < 0.5 and abs(h-70) < 0.5 else "FAIL")
    print("Type3 fonts:", len(re.findall(rb"/Subtype\s*/Type3", t)), " TrueType/CIDFontType2:", len(re.findall(rb"/Subtype\s*/(?:TrueType|CIDFontType2)", t)), " FontFile2:", len(re.findall(rb"/FontFile2", t)), " path ops (fills 'f'/strokes 'S') present:", len(re.findall(rb"\n(?:f|S|f\*|B)\n", t)))
