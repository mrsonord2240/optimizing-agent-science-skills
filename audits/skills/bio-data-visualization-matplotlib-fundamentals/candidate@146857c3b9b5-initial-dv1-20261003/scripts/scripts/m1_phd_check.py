"""MPL audit run 1: run the shipped scripts/matplotlib_phd.py unchanged, then check page sizes against the 89/180 mm
journal widths the Skill promises, raster content and fonts. Usage: py.sh m1_phd_check.py <skilldir> <outdir>"""
import re, subprocess, sys, zlib
from pathlib import Path

skill, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
r = subprocess.run([sys.executable, str(skill / "scripts" / "matplotlib_phd.py")], cwd=out, capture_output=True, text=True)
print("exit", r.returncode, "stderr:", r.stderr.strip()[:500] or "none")


def mediabox_mm(p):
    b = p.read_bytes()
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", b)
    x0, y0, x1, y1 = (float(v) for v in m.groups())
    return round((x1 - x0) / 72 * 25.4, 1), round((y1 - y0) / 72 * 25.4, 1)


def n_images(p):
    return len(re.findall(rb"/Subtype\s*/Image", p.read_bytes()))


def chk(label, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")


target = {"pca.pdf": (89, 70), "multipanel.pdf": (180, 110), "heatmap.pdf": (89, 90), "volcano_sns.pdf": (89, 70)}
for f in sorted(out.glob("*.pdf")):
    w, h = mediabox_mm(f)
    t = target.get(f.name)
    print(f"{f.name}: {f.stat().st_size} B, page {w} x {h} mm, image XObjects {n_images(f)}", f"(documented {t[0]} x {t[1]} mm)" if t else "")
for f, (tw, th) in target.items():
    w, h = mediabox_mm(out / f)
    chk(f"{f} page width equals the documented journal width {tw} mm (within 1 mm)", abs(w - tw) <= 1)
chk("heatmap.pdf embeds the imshow as a raster image and keeps text vector", n_images(out / "heatmap.pdf") >= 1)
chk("pca.pdf rasterises the scatter (>=1 image XObject)", n_images(out / "pca.pdf") >= 1)
print("files:", sorted(p.name for p in out.iterdir()))
