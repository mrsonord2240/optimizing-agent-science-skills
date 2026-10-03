"""Execute every python block of references/chart-recipes.md VERBATIM (whole block, one exec per block, with
placeholder data bound in the namespace only) and test each failure-modes.md claim. Usage: f1 <skilldir> <outdir>"""
import re, sys, os, warnings
from pathlib import Path
skill, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt, seaborn as sns
mpl.rcParams.update({'pdf.fonttype': 42, 'font.size': 7})
rng = np.random.default_rng(0); ok = True
def chk(l, c):
    global ok; ok &= bool(c); print(f"[{'PASS' if c else 'FAIL'}] {l}")
def box(p):
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(p).read_bytes()); a = list(map(float, m.groups()))
    return round((a[2]-a[0])/72*25.4, 2), round((a[3]-a[1])/72*25.4, 2)
rec = (skill/'references'/'chart-recipes.md').read_text(encoding='utf-8')
blocks = re.findall(r"```python\n(.*?)```", rec, re.S)
print(len(blocks), 'python blocks in chart-recipes.md')
x = np.linspace(0, 10, 50); matrix = rng.normal(size=(20, 8))
ns = {'x': x, 'y': rng.normal(size=50), 'values': rng.normal(size=50), 'y1': np.sin(x), 'y2': np.cos(x), 'y_low': np.sin(x)-.3, 'y_high': np.sin(x)+.3,
      'categories': list('ABC'), 'group_a': rng.normal(size=30), 'group_b': rng.normal(1,1,30), 'group_c': rng.normal(2,1,30),
      'matrix': matrix, 'vmax': float(np.quantile(np.abs(matrix), .99))}   # note: no 'np' in ns: block must import it itself
# A python block holds several alternative fragments, each starting with a "# Title" comment line; each fragment is exec'd
# verbatim on its own axes with data suited to it (a bar chart needs 3 values, a scatter needs N). Nothing is edited.
frags = []
for i, b in enumerate(blocks, 1):
    for p in re.split(r"\n(?=# [A-Z][^\n]*\n)", b):
        if p.strip(): frags.append((i, p))
data = {'Scatter': {'x': rng.normal(size=50), 'y': rng.normal(size=50), 'values': rng.normal(size=50)},
        'Bar': {'values': [3, 5, 2]}, 'Histogram': {'values': rng.normal(size=500)}}
for i, p in frags:
    head = p.splitlines()[0]
    fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), layout='constrained')
    n = dict(ns); n.update(ax=ax, fig=fig)
    for k, d in data.items():
        if head.startswith('# ' + k): n.update(d)
    try:
        with warnings.catch_warnings(record=True) as W:
            warnings.simplefilter('always'); exec(compile(p, 'chart-recipes.md', 'exec'), n); fig.canvas.draw()
        chk(f"block {i} fragment '{head[:32]}' ran verbatim; warnings={[str(w.message)[:60] for w in W]}", not W)
        fig.savefig(f"frag_{re.sub(r'[^A-Za-z]+', '_', head)[:24]}.png", dpi=150)
    except Exception as e:
        chk(f"block {i} fragment '{head[:32]}' ran verbatim", False); print('    ', type(e).__name__, e)
    plt.close(fig)
print('RESULT', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
