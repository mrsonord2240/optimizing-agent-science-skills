"""Root cause of the savefig TypeError in the Skill's python block: show_counts=True + numpy 2.5.3, and what works instead."""
import warnings; warnings.filterwarnings('ignore')
import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from upsetplot import from_contents, UpSet
print('numpy', np.__version__, 'matplotlib', matplotlib.__version__)
try:
    float(np.array([1.0])); print('float(np.array([1.0])): ok')
except Exception as e:
    print('float(np.array([1.0])) ->', type(e).__name__, e)
sets = {'SetA': ['Gene1','Gene2','Gene3','Gene4'], 'SetB': ['Gene2','Gene3','Gene5','Gene6'], 'SetC': ['Gene1','Gene3','Gene6','Gene7']}
data = from_contents(sets)
OUT = 'F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/'
for sc, sp in [(True, False), (False, False), ('{:d}', False), (True, True)]:
    fig = plt.figure(figsize=(8, 5)); u = UpSet(data, subset_size='count', show_counts=sc, show_percentages=sp, facecolor='#0072B2', element_size=40)
    try:
        u.plot(fig=fig); fig.savefig(OUT + 'i3b_tmp.png', dpi=60); print(f'show_counts={sc!r:8} show_percentages={sp}: savefig OK')
    except Exception as e:
        print(f'show_counts={sc!r:8} show_percentages={sp}: savefig FAILS -> {type(e).__name__}: {str(e)[:70]}')
    plt.close(fig)
