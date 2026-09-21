"""The shipped example's 'UpSet with metadata' part: (1) as shipped, (2) minimal repair, (3) check add_catplot medians vs independent per-intersection medians. PYENV=venv-pd2, show_counts=False."""
import sys, warnings; warnings.filterwarnings('ignore')
sys.path.insert(0, 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run')
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from upsetplot import from_contents, UpSet
from up_helpers import extract
OUT = 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/'
np.random.seed(42)
all_genes = [f'Gene{i}' for i in range(1, 501)]
gene_sets = {'Treatment_A': np.random.choice(all_genes, 150, replace=False).tolist(), 'Treatment_B': np.random.choice(all_genes, 130, replace=False).tolist(),
             'Timepoint_Early': np.random.choice(all_genes, 100, replace=False).tolist(), 'Timepoint_Late': np.random.choice(all_genes, 180, replace=False).tolist(),
             'Pathway_Response': np.random.choice(all_genes, 90, replace=False).tolist()}
data = from_contents(gene_sets)
print('from_contents returns:', type(data).__name__, list(data.columns), 'index names', list(data.index.names)[:3], '...')
try:
    data.to_frame(); print('to_frame OK')
except Exception as e:
    print('AS SHIPPED  data.to_frame() ->', type(e).__name__, e)
# minimal repair: attach attributes to the DataFrame from_contents returned (index already the membership MultiIndex)
rng = np.random.default_rng(42); df = data.copy(); df['log2FC'] = rng.normal(0, 1.5, len(df))
try:
    u = UpSet(df, subset_size='count', show_counts=False, sort_by='cardinality'); u.add_catplot(value='log2FC', kind='box', color='#E64B35')
    fig = plt.figure(figsize=(14, 10)); ax = u.plot(fig=fig); fig.savefig(OUT + 'i3d_catplot_repaired.png', dpi=80, bbox_inches='tight')
    print('repaired version: draws; axes:', list(ax.keys()))
    ex = extract(ax); print('  bars drawn:', len(ex['heights']), ' sum of bars == number of genes in union:', int(sum(ex['heights'])) == len(df))
    # independent median per intersection vs the boxplot medians drawn
    cat_ax = [a for k, a in ax.items() if k.startswith('extra')][0]
    med = [l.get_ydata()[0] for l in cat_ax.lines if len(set(l.get_ydata())) == 1 and len(l.get_xdata()) == 2 and abs(l.get_xdata()[1] - l.get_xdata()[0]) > 0.2 and abs(l.get_xdata()[1] - l.get_xdata()[0]) < 0.9]
    print('  boxplot median lines found:', len(med), '(bars:', len(ex['heights']), ')')
    grp = df.groupby(level=list(range(5)))['log2FC'].median()
    true_by_members = {tuple(n for n, f in zip(df.index.names, k) if f): v for k, v in grp.items()}
    want = [true_by_members[tuple(m) if False else tuple(n for n in df.index.names if n in m)] for m in ex['members']]
    print('  drawn medians == independent group medians (order by column):', np.allclose(sorted(med), sorted(want), atol=1e-6) if len(med) == len(want) else 'count mismatch')
except Exception as e:
    print('repaired version FAILS:', type(e).__name__, str(e)[:120])
