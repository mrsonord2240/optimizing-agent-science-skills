"""Input 3: Python upsetplot route. SKILL.md block verbatim (3 sets) + checks; then the planted 8-set data with the parameters the Skill teaches.
Run with PYENV=venv-pd2 (upsetplot 0.9.0 needs pandas 2)."""
import sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run')
import matplotlib.pyplot as plt
import pandas as pd
from up_helpers import read_sets, truth, extract
OUT = 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/'
print('pandas', pd.__version__)

# ---------------- SKILL.md python block, VERBATIM (savefig path moved to OUT) ----------------
from upsetplot import from_contents, UpSet
import matplotlib.pyplot as plt

sets = {'SetA': ['Gene1','Gene2','Gene3','Gene4'],
        'SetB': ['Gene2','Gene3','Gene5','Gene6'],
        'SetC': ['Gene1','Gene3','Gene6','Gene7']}
data = from_contents(sets)

upset = UpSet(data,
              subset_size='count',
              show_counts=True,
              sort_by='cardinality',                    # 'cardinality' OR 'degree'
              sort_categories_by='cardinality',
              facecolor='#0072B2',
              element_size=40)
upset.style_subsets(present=['SetA', 'SetB'], facecolor='#D55E00')   # highlight specific intersection
fig = plt.figure(figsize=(8, 5))
axes = upset.plot(fig=fig)
try:
    plt.savefig(OUT + 'i3a_skill_block.pdf', bbox_inches='tight')
    print('VERBATIM block: savefig OK')
except Exception as e:      # recorded, then re-run with show_counts=False (see i3b_showcounts_rootcause.py)
    print('VERBATIM block: savefig FAILS ->', type(e).__name__, str(e)[:80])
    plt.close('all')
    upset = UpSet(data, subset_size='count', show_counts=False, sort_by='cardinality', sort_categories_by='cardinality',
                  facecolor='#0072B2', element_size=40)
    upset.style_subsets(present=['SetA', 'SetB'], facecolor='#D55E00')
    fig = plt.figure(figsize=(8, 5)); axes = upset.plot(fig=fig)
    plt.savefig(OUT + 'i3a_skill_block.pdf', bbox_inches='tight')
plt.savefig(OUT + 'i3a_skill_block.png', bbox_inches='tight', dpi=100)
# ---------------- end block ----------------

ex = extract(axes)
T = truth(sets)
tex = {c: v[0] for c, v in T.items() if v[0] > 0}
print('drawn columns (members, height, label, bar colour):')
for m, h, l, c in zip(ex['members'], ex['heights'], ex['labels'], ex['bar_colors']):
    print('  ', m, h, l, c)
drawn = {tuple(sorted(m)): h for m, h in zip(ex['members'], ex['heights'])}
print('P1 every drawn bar == exclusive truth and no missing intersection:', drawn == {tuple(sorted(k)): v for k, v in tex.items()})
print('P2 set totals == list lengths:', ex['totals'] == {k: float(len(v)) for k, v in sets.items()}, ex['totals'])
print('P3 count labels == heights:', [int(x) for x in ex['labels']] == [int(h) for h in ex['heights']])
orange = [m for m, c in zip(ex['members'], ex['bar_colors']) if c.lower() == '#d55e00']
print('P4 bars coloured #D55E00 by style_subsets(present=[SetA,SetB]):', orange)
print('   Skill comment says "highlight specific intersection": exact A&B (not C) is', ('SetA', 'SetB') in orange, '; superset A&B&C also highlighted:', ('SetA', 'SetB', 'SetC') in orange)
print('   pdf size', __import__('os').path.getsize(OUT + 'i3a_skill_block.pdf'))
plt.close('all')
