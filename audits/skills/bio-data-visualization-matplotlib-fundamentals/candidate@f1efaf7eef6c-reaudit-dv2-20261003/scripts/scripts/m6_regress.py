"""Re-audit m6: first-loop regressions MPL-005 (Okabe-Ito cluster colours, no redundant panel titles, text sizes) and MPL-006 (no pyplot state calls in the shipped text).
Usage: py.sh m6_regress.py <skilldir> <outdir>"""
import re, runpy, sys, os
from pathlib import Path
skill, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt, matplotlib.colors as mc
ok = True
def chk(l, c):
    global ok; ok &= bool(c); print(f"[{'PASS' if c else 'FAIL'}] {l}"); return c
g = runpy.run_path(str(skill/'scripts'/'matplotlib_phd.py'), run_name='__main__')
okabe = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#000000']
expected = {mc.to_hex(okabe[i]).lower() for i in (0, 1, 2, 4)}
figs = [plt.figure(n) for n in plt.get_fignums()]; print('figures:', [(len(f.axes), tuple(round(x * 25.4) for x in f.get_size_inches())) for f in figs])
pca = [f for f in figs if len(f.axes) == 1 and f.axes[0].get_xlabel().startswith('PC1')][0]
cols = {mc.to_hex(c).lower() for col in pca.axes[0].collections for c in col.get_facecolors()}
print('pca cluster colours:', sorted(cols)); chk("PCA cluster colours are the four Okabe-Ito colours the script names (yellow skipped)", cols == expected)
grid = [f for f in figs if len(f.axes) == 6][0]
chk("grid panels carry no titles (only the a-f tags)", all(a.get_title() == '' for a in grid.axes))
tags = [t.get_text() for a in grid.axes for t in a.texts]; chk("panel tags a-f present", tags == list('abcdef'))
sizes = sorted({round(t.get_fontsize(), 1) for f in figs for t in f.findobj(mpl.text.Text) if t.get_visible() and t.get_text().strip()})
print('text sizes:', sizes); chk("visible text only 6 and 7 pt in all five figures", set(sizes) <= {6.0, 7.0})
# MPL-006: pyplot state calls in shipped text
bad = []
for f in ['SKILL.md', 'usage-guide.md', 'references/chart-recipes.md', 'scripts/matplotlib_phd.py']:
    for n, line in enumerate((skill / f).read_text(encoding='utf-8').splitlines(), 1):
        if re.search(r"\bplt\.(imshow|colorbar|scatter|plot|xlabel|ylabel|title|bar|hist)\(", line) and 'plt.xlabel' not in line.split('#')[-1] and not line.lstrip().startswith(('-', '#', '|')) and '`' not in line:
            bad.append((f, n, line.strip()[:80]))
print('pyplot state calls in code lines:', bad or 'none'); chk("no pyplot state-machine plotting calls in shipped code", not bad)
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
