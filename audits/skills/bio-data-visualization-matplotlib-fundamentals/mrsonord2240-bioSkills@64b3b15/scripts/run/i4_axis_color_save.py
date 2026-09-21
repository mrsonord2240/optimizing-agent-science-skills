"""Input 4 (Variant B): 'Log-scale y axis with sci-notation x ticks and a date axis; CVD-safe colours (Okabe-Ito, batlow, symmetric RdBu_r for LFC); then export PDF, PNG 300 dpi, TIFF LZW, SVG.'
SYNTHETIC. SKILL.md blocks 4, 5, 6 exec'd verbatim statement-groups; failures recorded."""
import os, sys, warnings, datetime as dt
os.makedirs('out', exist_ok=True); os.chdir('out'); sys.path.insert(0, '..')
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from blocks import blocks
B = blocks(); exec(B[0])
rng = np.random.default_rng(3)

def run(name, code, ns, note=''):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try: exec(code, ns); st = 'ok'
        except Exception as e: st = f'{type(e).__name__}: {str(e)[:200]}'
    ws = sorted({f'{x.category.__name__}: {str(x.message)[:120]}' for x in w})
    print(f'[{name}] {st} | warnings={ws} {note}')
    return st

# ---- block 4, statement by statement, np deliberately NOT in namespace
fig, ax = plt.subplots(constrained_layout=True)
ax.plot(np.arange(1, 11), 10.0 ** np.arange(1, 11)); 
segs = [s for s in B[4].split('\n\n') if s.strip()]
for s in segs:
    ns = dict(ax=ax, plt=plt)
    run('b4:' + s.strip().splitlines()[0][:30], s, ns)
# with np supplied (fair to the Skill)
fig, ax = plt.subplots(constrained_layout=True); ax.plot(np.arange(10), np.arange(10))
for s in segs[2:4]:
    st = run('b4+np:' + s.strip().splitlines()[0][:30], s, dict(ax=ax, plt=plt, np=np))
print('tick locs after set_xticks', ax.get_xticks(), 'labels', [t.get_text() for t in ax.get_xticklabels()])
# proper date axis
fig, ax = plt.subplots(constrained_layout=True)
d = [dt.date(2026, 1, 1) + dt.timedelta(days=30 * i) for i in range(12)]
ax.plot(d, rng.normal(size=12).cumsum())
import matplotlib.dates as mdates
run('b4 date formatter on real dates', segs[2].split('\n')[0:0] and '' or "ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))", dict(ax=ax, mdates=mdates))
fig.canvas.draw(); print('date tick labels', [t.get_text() for t in ax.get_xticklabels()][:4])
# sci notation: does ScalarFormatter(useMathText) alone give sci-notation?
fig, ax = plt.subplots(constrained_layout=True); ax.plot([0, 2e6, 4e6], [1, 2, 3])
from matplotlib.ticker import ScalarFormatter
ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True)); fig.canvas.draw()
print('sci block: tick labels', [t.get_text() for t in ax.get_xticklabels()], '| offset text', repr(ax.xaxis.get_offset_text().get_text()))
# log scale
fig, ax = plt.subplots(constrained_layout=True); ax.plot([1, 10, 100, 1000], [1, 10, 100, 1000]); ax.set_yscale('log'); fig.canvas.draw()
print('log y ticks', ax.get_yticks(), 'scale', ax.get_yscale())

# ---- block 5 colour
data = rng.normal(size=(40, 30)) * 3
ns = dict(np=np, plt=plt, data=data)
st = run('b5 whole (data supplied, np supplied)', B[5], ns)
okabe = ns['okabe_ito']; print('okabe_ito', len(okabe), 'colours; unique', len(set(okabe)))
vmax = np.quantile(np.abs(data), 0.99); im = plt.gci(); print('symmetric clim', im.get_clim(), 'expected +/-', round(vmax, 4))
# Okabe-Ito published hexes
OI_ref = {'orange': '#E69F00', 'skyblue': '#56B4E9', 'green': '#009E73', 'yellow': '#F0E442', 'blue': '#0072B2', 'vermillion': '#D55E00', 'purple': '#CC79A7', 'black': '#000000'}
print('okabe-ito hexes match published set:', sorted(okabe) == sorted(OI_ref.values()))
run('b5 without data defined', B[5], dict(np=np, plt=plt))

# ---- block 6 saving
fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
ax.scatter(rng.normal(size=3000), rng.normal(size=3000), s=6, rasterized=True); ax.set_xlabel('Sample PC1 axis label'); ax.set_ylabel('y')
ns = dict(fig=fig)
for s in B[6].split('\n\n'):
    run('b6:' + s.strip().splitlines()[0][:40], s, ns)
from PIL import Image
from pdfcheck import pdf_info, pdf_text
print('PDF', pdf_info('figure.pdf'))
im = Image.open('figure.png'); print('PNG', im.size, im.info.get('dpi'), '=> at 300 dpi width mm', round(im.size[0]/300*25.4, 2))
t = Image.open('figure.tiff'); print('TIFF', t.size, t.info.get('dpi'), 'compression', t.info.get('compression'))
svg = open('figure.svg', encoding='utf-8').read()
print('SVG bytes', len(svg), '| contains <text> elements:', svg.count('<text'), '| label string present as text:', 'Sample PC1 axis label' in svg, '| <path> count', svg.count('<path'), '| svg.fonttype default', mpl.rcParams['svg.fonttype'])
print('PDF text:', repr(pdf_text('figure.pdf')[:80]))
