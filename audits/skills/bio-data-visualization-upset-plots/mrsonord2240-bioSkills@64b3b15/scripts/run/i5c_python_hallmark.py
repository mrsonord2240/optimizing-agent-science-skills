"""Python route on the REAL Hallmark 10-set data (data/hallmark10_sets.tsv written by i5): same truth as R. PYENV=venv-pd2, show_counts=False."""
import sys, warnings; warnings.filterwarnings('ignore')
sys.path.insert(0, 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run')
import matplotlib.pyplot as plt
from upsetplot import from_contents, UpSet
from up_helpers import read_sets, truth, extract
sets = read_sets('F:/OpenScience/audits/bio-data-visualization-upset-plots/data/hallmark10_sets.tsv')
T = truth(sets); tex = sorted([v[0] for c, v in T.items() if v[0] > 0], reverse=True)
print('non-empty exclusive intersections (set-op truth):', len(tex), ' top20:', tex[:20])
data = from_contents(sets)
u = UpSet(data, subset_size='count', show_counts=False, sort_by='cardinality', sort_categories_by='cardinality', max_subset_rank=20, facecolor='#0072B2', element_size=40)
fig = plt.figure(figsize=(14, 7)); ax = u.plot(fig=fig); fig.savefig('F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/i5c_hallmark_py.png', dpi=100, bbox_inches='tight')
ex = extract(ax)
print('drawn heights:', [int(h) for h in ex['heights']])
print('W1 == top-20 truth:', [int(h) for h in ex['heights']] == tex[:20])
print('W2 each drawn bar equals the exclusive size of its drawn membership:', all(T[tuple(s for s in sets if s in m)][0] == h for m, h in zip(ex['members'], ex['heights'])))
print('W3 totals == set sizes:', ex['totals'] == {k: float(len(set(v))) for k, v in sets.items()})
