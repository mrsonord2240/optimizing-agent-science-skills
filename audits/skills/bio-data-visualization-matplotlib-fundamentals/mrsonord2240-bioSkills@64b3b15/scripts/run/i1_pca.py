"""Input 1 (canonical): 'Make a Nature single-column PCA scatter of my RNA-seq samples, 89 mm, TrueType-embedded PDF, rasterized points'
SYNTHETIC data: 3000 cells x 200 genes, 3 groups with a planted mean shift; PCA by sklearn so the axis labels can be checked against real variance.
SKILL.md code blocks 0 and 1 are exec'd verbatim (extracted by blocks.py), not retyped."""
import os, warnings
os.makedirs('out', exist_ok=True); os.chdir('out')
warnings.simplefilter('always')
import numpy as np, matplotlib as mpl
from sklearn.decomposition import PCA
from blocks import blocks  # noqa
import sys; sys.path.insert(0, '..')
B = blocks()
rng = np.random.default_rng(42)
n, g = 3000, 200
grp = rng.integers(0, 3, n)
shift = rng.normal(size=(3, g)) * 1.5
X = rng.normal(size=(n, g)) + shift[grp]
pca = PCA(2).fit(X)
pc = pca.transform(X); x, y = pc[:, 0], pc[:, 1]
ev = pca.explained_variance_ratio_ * 100
print('PCA explained variance %', ev.round(2))
# block 0: rcParams (verbatim)
exec(B[0])
print('after rcParams: pdf.fonttype', mpl.rcParams['pdf.fonttype'], 'savefig.bbox', mpl.rcParams['savefig.bbox'])
# block 1: single axes (verbatim), then grid of axes
data = {c: {'x': rng.normal(size=100), 'y': rng.normal(size=100)} for c in 'ABCDEF'}
exec(B[1].replace("ax.set_xlabel('PC1 (45%)')", "ax.set_xlabel('PC1 (45%)')"))  # verbatim; hard-coded labels kept on purpose
import matplotlib.pyplot as plt
# record what verbatim code did
print('n figures open', len(plt.get_fignums()))
# now the corrected labelled version (what a careful agent would do) -> second figure for comparison
fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
ax.scatter(x, y, c=grp, cmap='viridis', s=10, alpha=0.7, edgecolors='none', rasterized=True)
ax.set_xlabel(f'PC1 ({ev[0]:.1f}%)'); ax.set_ylabel(f'PC2 ({ev[1]:.1f}%)')
ax.spines[['top', 'right']].set_visible(False)
print('figure size in (as built):', fig.get_size_inches(), '-> mm', fig.get_size_inches()*25.4)
fig.savefig('pca_true.pdf'); fig.savefig('pca_true.png')
print('xlim', ax.get_xlim(), 'data x range', x.min(), x.max())
print('xlabel', ax.get_xlabel(), '| ylabel', ax.get_ylabel())
print('hard-coded label "PC1 (45%)" vs real', round(ev[0],1))
from pdfcheck import pdf_info, pdf_text
for f in ['scatter.pdf', 'pca_true.pdf']:
    print(f, pdf_info(f))
print('text of pca_true.pdf:', repr(pdf_text('pca_true.pdf')))
from PIL import Image
im = Image.open('pca_true.png'); print('PNG pixels', im.size, 'dpi', im.info.get('dpi'))
a = np.asarray(im.convert('L')); print('nonwhite frac', round((a < 250).mean(), 3))
