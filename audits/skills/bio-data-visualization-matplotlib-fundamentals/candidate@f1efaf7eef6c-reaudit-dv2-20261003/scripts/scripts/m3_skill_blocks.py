"""Re-audit m3 (adapted from the dv1 re-audit script r3_skill_blocks.py): execute every ```python block of SKILL.md verbatim on the REAL airway DESeq2 table (rows reordered three ways); check colour->category
binding per drawn point, saved page size/px for pdf/png/tiff/svg/eps, SVG <text>, rasterisation. Usage: py.sh r3_skill_blocks.py <skilldir> <outdir>"""
import re, sys, os, copy
from pathlib import Path
skill, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.colors as mc, matplotlib.pyplot as plt
ok = True
def chk(l, c):
    global ok; ok &= bool(c); print(f"[{'PASS' if c else 'FAIL'}] {l}"); return c
AIR = "F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv"
raw = pd.read_csv(AIR); print("airway rows", len(raw), "after dropna(padj,pvalue):", len(raw.dropna(subset=['padj','pvalue'])))
res = raw.dropna(subset=['padj','pvalue']).copy()
res['log_fold_change'] = res.log2FoldChange; res['neg_log_p'] = -np.log10(res.pvalue)
res['significance'] = np.where((res.padj<.05)&(res.log2FoldChange>1),'Up',np.where((res.padj<.05)&(res.log2FoldChange<-1),'Down','NS'))
print(res.significance.value_counts().to_dict())
text = (skill/'SKILL.md').read_text(encoding='utf-8')
blocks = re.findall(r"```python\n(.*?)```", text, re.S); print(len(blocks), "python blocks")
rng = np.random.default_rng(1)
def fresh(df):
    return {'df': df, 'x': rng.normal(size=2000), 'y': rng.normal(size=2000), 'data': rng.normal(size=(30,12)),
            'panel_data': {k: {'x': rng.normal(size=50), 'y': rng.normal(size=50)} for k in 'abcdef'}}
def box(p):
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(p).read_bytes()); a = list(map(float, m.groups()))
    return round((a[2]-a[0])/72*25.4, 2), round((a[3]-a[1])/72*25.4, 2)
# --- run all blocks in order once (Up-first ordering)
orders = {'upfirst': res.sort_values('significance', key=lambda c: c.map({'Up':0,'Down':1,'NS':2})),
          'nsfirst': res.sort_values('significance', key=lambda c: c.map({'NS':0,'Down':1,'Up':2})),
          'shuffled': res.sample(frac=1, random_state=3)}
pal = {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'}
sns_i = [i for i, b in enumerate(blocks) if 'sns.scatterplot' in b][0]
for oname, df in orders.items():
    df = df.reset_index(drop=True); print(f"--- ordering {oname}: first-appearance order {list(dict.fromkeys(df.significance))}")
    ns = fresh(df); plt.close('all')
    for i, b in enumerate(blocks):
        try: exec(compile(b, f'SKILL.md#block{i}', 'exec'), ns)
        except Exception as e: chk(f"block {i} runs verbatim ({oname})", False); print("   ", type(e).__name__, e); raise
    chk(f"all {len(blocks)} blocks ran verbatim ({oname})", True)
    # find the scatterplot figure (axes with hue legend)
    target = None
    for n in plt.get_fignums():
        ax = plt.figure(n).axes[0]
        if ax.get_legend() is not None and ax.get_xlabel() == 'log_fold_change': target = ax
    chk(f"seaborn recipe figure found ({oname})", target is not None)
    col = target.collections[0]; fc = col.get_facecolors(); n_pts = len(df)
    chk(f"points drawn == rows ({oname}): {len(fc)} vs {n_pts}", len(fc) == n_pts)
    exp = np.array([mc.to_rgb(pal[s]) for s in df.significance]); got = fc[:, :3]
    chk(f"every drawn point has its class colour ({oname}); mismatches={int((np.abs(exp-got).max(axis=1)>1e-6).sum())}", (np.abs(exp-got).max(axis=1) < 1e-6).all())
    lg = target.get_legend(); lgmap = {t.get_text(): mc.to_hex(h.get_color()).lower() for t, h in zip(lg.get_texts(), lg.legend_handles)}
    print("   legend:", lgmap)
    chk(f"legend text->colour matches palette ({oname})", all(lgmap.get(k, '').lower() == v.lower() for k, v in pal.items() if k in lgmap) and set(lgmap) >= {'Up','Down','NS'})
    # seaborn.objects expression: the block ends with an un-rendered Plot; re-evaluate its source and render
    import seaborn.objects as so
    pl = (so.Plot(df, x='log_fold_change', y='neg_log_p').add(so.Dots(pointsize=2), color='significance').scale(color=pal)).plot()
    lgs = pl._figure.legends
    lm = {t.get_text(): mc.to_hex(h.get_edgecolor()[0] if hasattr(h, 'get_edgecolor') and len(h.get_edgecolor()) else h.get_color()).lower() for t, h in zip(lgs[0].get_texts(), lgs[0].legend_handles)} if lgs else {}
    print("   so legend:", lm)
    plt.close('all')
# --- page sizes / files from the final sequential run (shuffled)
print(sorted(os.listdir('.')))
chk(f"scatter.pdf page {box('scatter.pdf')} mm == 89 wide x 70", abs(box('scatter.pdf')[0]-89) <= .3 and abs(box('scatter.pdf')[1]-70) <= .3)
# --- Saving block against an 89 x 70 mm figure
save_block = [b for b in blocks if 'figure.tiff' in b][0]
plt.close('all')
fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), layout='constrained'); ax.plot([0, 1], [0, 1]); ax.set_xlabel('x label'); ax.set_title('t')
ns = {'fig': fig, 'mpl': mpl, 'plt': plt}; exec(compile(save_block, 'SKILL.md#saving', 'exec'), ns)
w, h = box('figure.pdf'); chk(f"figure.pdf page {w} x {h} mm == 89 x 70", abs(w-89) <= .3 and abs(h-70) <= .3)
from PIL import Image
for f in ('figure.png', 'figure.tiff'):
    im = Image.open(f); print(f, im.size, im.info.get('dpi'), getattr(im, 'compression', None) or im.info.get('compression'))
    chk(f"{f} width {im.size[0]} px == 89 mm @300 dpi (1051)", abs(im.size[0] - round(89/25.4*300)) <= 2)
chk("tiff compression is tiff_lzw", Image.open('figure.tiff').info.get('compression') == 'tiff_lzw')
svg = Path('figure.svg').read_text(encoding='utf-8'); nt = len(re.findall(r'<text[ >]', svg)); print('svg <text> elements:', nt)
chk("figure.svg has <text> elements", nt > 0)
# control: default svg.fonttype -> paths
fig.savefig('control_default.svg'); c = Path('control_default.svg').read_text(encoding='utf-8'); print('control (default fonttype) <text> elements:', len(re.findall(r'<text[ >]', c)))
chk("control default SVG has 0 <text>", len(re.findall(r'<text[ >]', c)) == 0)
# EPS (claimed ps.fonttype=42 relevant)
import warnings
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always'); fig.savefig('figure.eps')
print('eps warnings:', [str(x.message)[:90] for x in W]); print('eps bbox:', re.search(rb'%%BoundingBox: .*', Path('figure.eps').read_bytes()).group().decode())
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
