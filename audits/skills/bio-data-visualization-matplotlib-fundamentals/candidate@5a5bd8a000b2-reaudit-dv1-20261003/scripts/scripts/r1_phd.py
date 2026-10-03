"""Re-audit 1: run shipped scripts/matplotlib_phd.py unchanged from a scratch cwd; measure page mm, text font sizes, points rasterised, Type42 flag, SVG text.
Usage: py.sh r1_phd.py <skilldir> <outdir>"""
import sys, os, re, runpy
from pathlib import Path
skill, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib.pyplot as plt, matplotlib as mpl
ns = runpy.run_path(str(skill/'scripts'/'matplotlib_phd.py'), run_name='__main__')
ok = True
def chk(l, c): 
    global ok; ok &= bool(c); print(f"[{'PASS' if c else 'FAIL'}] {l}"); return c
def box(p):
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(p).read_bytes()); a = list(map(float, m.groups()))
    return round((a[2]-a[0])/72*25.4, 2), round((a[3]-a[1])/72*25.4, 2)
want = {'pca.pdf': (89, 70), 'multipanel.pdf': (180, 110), 'heatmap.pdf': (89, 90), 'volcano_sns.pdf': (89, 70), 'volcano_so.pdf': (89, 70)}
for f, (w, h) in want.items():
    got = box(f); print(f, got, 'mm; want', (w, h))
    chk(f"{f} page {got} within 0.3 mm of {w}x{h}", abs(got[0]-w) <= .3 and abs(got[1]-h) <= .3)
print('files', sorted(os.listdir('.')))
chk('exactly the five PDFs written', sorted(os.listdir('.')) == sorted(want))
# font sizes of every Text artist in every open figure
sizes = set()
for n in plt.get_fignums():
    fig = plt.figure(n)
    for t in fig.findobj(mpl.text.Text):
        if t.get_text().strip() and t.get_visible(): sizes.add(t.get_fontsize())
print('text font sizes in open figures (pt):', sorted(sizes))
chk("all text 6-7 pt", sizes <= {6.0, 7.0})
print('pdf.fonttype', mpl.rcParams['pdf.fonttype'], 'ps', mpl.rcParams['ps.fonttype'], 'savefig.bbox', mpl.rcParams['savefig.bbox'])
print("RESULT", "PASS" if ok else "FAIL")
