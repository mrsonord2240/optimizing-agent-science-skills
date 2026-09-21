"""Input 3 (cont.): upsetplot on SYNTHETIC planted 8-set data (D subset of A, H empty). show_counts=False everywhere (see i3b). PYENV=venv-pd2."""
import sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run')
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from upsetplot import from_contents, from_memberships, UpSet
from up_helpers import read_sets, truth, extract
OUT = 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/'
D = 'F:/OpenScience/audits/bio-data-visualization-upset-plots/data/'
sets = read_sets(D + 'planted_sets.tsv'); sets = {k: sets.get(k, []) for k in 'ABCDEFGH'}
print({k: len(v) for k, v in sets.items()})
T = truth(sets); tex = {tuple(sorted(c)): v[0] for c, v in T.items() if v[0] > 0}
key = lambda m: tuple(sorted(m))

def draw(u, name, w=12, h=6):
    fig = plt.figure(figsize=(w, h)); ax = u.plot(fig=fig); fig.savefig(OUT + name, dpi=100, bbox_inches='tight'); plt.close(fig); return ax

# (a) from_contents with an empty list
try:
    data = from_contents(sets); print('from_contents with empty H OK; index names:', list(data.index.names), 'rows', len(data))
except Exception as e:
    print('from_contents with empty H FAILS:', type(e).__name__, e); sets_ne = {k: v for k, v in sets.items() if v}; data = from_contents(sets_ne)
    print('   retry without H: index names', list(data.index.names))

# (b) skill args, sort by cardinality
u = UpSet(data, subset_size='count', show_counts=False, sort_by='cardinality', sort_categories_by='cardinality', facecolor='#0072B2', element_size=40)
ax = draw(u, 'i3c_card.png'); ex = extract(ax)
drawn = {key(m): h for m, h in zip(ex['members'], ex['heights'])}
print('[cardinality] columns drawn:', len(ex['heights']), 'expected nonzero exclusive intersections:', len(tex))
print('Q1 every drawn bar == exclusive truth, none missing:', drawn == {k: float(v) for k, v in tex.items()})
print('Q2 heights non-increasing L->R:', all(np.diff(ex['heights']) <= 0), ex['heights'])
print('Q3 totals == set sizes:', ex['totals'] == {k: float(len(v)) for k, v in sets.items() if v}, ex['totals'])
print('   rows drawn (top->bottom):', ex['rows'])
print('Q4 empty set H shown as a row:', 'H' in ex['rows'])
print('Q5 D only ever with A:', not any('D' in m and 'A' not in m for m in ex['members']))

# (c) sort by degree
u = UpSet(data, subset_size='count', show_counts=False, sort_by='degree', sort_categories_by='cardinality'); ax = draw(u, 'i3c_degree.png'); ex = extract(ax)
dg = [len(m) for m in ex['members']]; print('\n[sort_by=degree] degrees L->R:', dg, 'heights:', ex['heights']); print('Q6 degree non-decreasing:', all(np.diff(dg) >= 0), ' non-increasing:', all(np.diff(dg) <= 0))
u = UpSet(data, subset_size='count', show_counts=False, sort_by='-degree'); ax = draw(u, 'i3c_negdegree.png'); ex = extract(ax); dg = [len(m) for m in ex['members']]; print('[sort_by=-degree] degrees:', dg)

# (d) filters
for kw in [dict(min_subset_size=4), dict(max_subset_rank=5), dict(min_degree=2), dict(max_degree=1), dict(min_degree=2, min_subset_size=3)]:
    u = UpSet(data, subset_size='count', show_counts=False, sort_by='cardinality', **kw); ax = draw(u, 'i3c_filter_%s.png' % '_'.join(f'{k}{v}' for k, v in kw.items())); ex = extract(ax)
    dr = {key(m): h for m, h in zip(ex['members'], ex['heights'])}
    ok = all(tex.get(k) == v for k, v in dr.items())
    exp = {k: v for k, v in tex.items() if (kw.get('min_subset_size') is None or v >= kw['min_subset_size']) and (kw.get('min_degree') is None or len(k) >= kw['min_degree']) and (kw.get('max_degree') is None or len(k) <= kw['max_degree'])}
    if 'max_subset_rank' in kw: exp = dict(sorted(exp.items(), key=lambda kv: -kv[1])[:kw['max_subset_rank']])
    print(f'[{kw}] drawn {len(dr)} cols, heights {ex["heights"]}; heights match truth: {ok}; count == filtered truth count: {len(dr)} vs {len(exp)}')

# (e) intersection_plot_elements: the shipped example says "Max intersections to show"
u = UpSet(data, subset_size='count', show_counts=False, sort_by='cardinality', intersection_plot_elements=3); ax = draw(u, 'i3c_ipe3.png'); ex = extract(ax)
print('\n[intersection_plot_elements=3] columns drawn:', len(ex['heights']), '(all 14 still drawn => it is a plot-height parameter, not a max-intersections cap)')
bb = ax['intersections'].get_position().height; u2 = UpSet(data, subset_size='count', show_counts=False, intersection_plot_elements=15); ax2 = draw(u2, 'i3c_ipe15.png')
print('   bar-panel height fraction  ipe=3:', round(bb, 3), ' ipe=15:', round(ax2['intersections'].get_position().height, 3))

# (f) style_subsets highlight semantics (present= vs exact)
u = UpSet(data, subset_size='count', show_counts=False, sort_by='cardinality', facecolor='#0072B2')
u.style_subsets(present=['A', 'B'], facecolor='#D55E00'); ax = draw(u, 'i3c_highlight_present.png'); ex = extract(ax)
print('\n[style_subsets(present=[A,B])] orange columns:', [m for m, c in zip(ex['members'], ex['bar_colors']) if c.lower() == '#d55e00'])
u = UpSet(data, subset_size='count', show_counts=False, sort_by='cardinality', facecolor='#0072B2')
u.style_subsets(present=['A', 'B'], absent=['C', 'D', 'E', 'F', 'G'], facecolor='#D55E00'); ax = draw(u, 'i3c_highlight_exact.png'); ex = extract(ax)
print('[style_subsets(present=[A,B], absent=rest)] orange columns:', [m for m, c in zip(ex['members'], ex['bar_colors']) if c.lower() == '#d55e00'])

# (g) duplicates inside a list: does from_contents inflate counts (Skill claims duplicates inflate counts silently)?
dup = {k: list(v) for k, v in sets.items() if v}; dup['A'] = dup['A'] + dup['A'][:6]
try:
    dd = from_contents(dup); u = UpSet(dd, subset_size='count', show_counts=False, sort_by='cardinality'); ax = draw(u, 'i3c_dups.png'); ex = extract(ax)
    dr = {key(m): h for m, h in zip(ex['members'], ex['heights'])}
    print('\n[duplicates in A] drawn A-only bar:', dr.get(('A',)), ' truth 12; totals A:', ex['totals'].get('A'), ' truth 30; matches truth:', dr == {k: float(v) for k, v in tex.items()})
except Exception as e:
    print('\n[duplicates in A] from_contents/plot raised:', type(e).__name__, str(e)[:100])

# (h) from_memberships (usage-guide) and from_indicators (SKILL failure-mode table)
mem = []
for g in sorted({g for v in sets.values() for g in v}):
    mem.append([k for k, v in sets.items() if g in v])
ms = from_memberships(mem); u = UpSet(ms, subset_size='count', show_counts=False, sort_by='cardinality'); ax = draw(u, 'i3c_memberships.png'); ex = extract(ax)
dr = {key(m): h for m, h in zip(ex['members'], ex['heights'])}
print('\n[from_memberships] drawn == exclusive truth:', dr == {k: float(v) for k, v in tex.items()})
from upsetplot import from_indicators
ind = pd.DataFrame({k: [g in set(v) for g in sorted({g for vv in sets.values() for g in vv})] for k, v in sets.items() if v})
fi = from_indicators(ind); u = UpSet(fi, subset_size='count', show_counts=False, sort_by='cardinality'); ax = draw(u, 'i3c_indicators.png'); ex = extract(ax)
dr = {key(m): h for m, h in zip(ex['members'], ex['heights'])}
print('[from_indicators] drawn == exclusive truth:', dr == {k: float(v) for k, v in tex.items()})
