"""Build a SYNTHETIC MaxQuant txt/ folder in which one run (T4) is a loading failure,
so PTXQC's own report can be asked whether it sees what the Skill says only raw-signal
inspection sees. Derived from the existing synthetic data/evidence.txt by scaling T4's
intensities and left-censoring its weakest identifications (the mechanism the SKILL.md
'Read the boxplots before normalizing' paragraph describes). proteinGroups.txt is the
already-failed data/proteinGroups_failed.txt. Nothing here is real measured data."""
import os, numpy as np, pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qc_failed')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20260915)

ev = pd.read_csv('../data/evidence.txt', sep='\t', low_memory=False)
t4 = ev['Raw file'] == 'T4'
sub = ev[t4].sort_values('Intensity')
drop = sub.index[: int(0.20 * len(sub))]          # left-censoring: weakest 20% fall below LOD
ev = ev.drop(index=drop)
t4 = ev['Raw file'] == 'T4'
ev.loc[t4, 'Intensity'] = ev.loc[t4, 'Intensity'] * 0.30   # 0.3x injection
ev = ev.reset_index(drop=True)
ev['id'] = range(len(ev))          # PTXQC validates that evidence 'id' is contiguous
ev.to_csv(os.path.join(OUT, 'evidence.txt'), sep='\t', index=False)

pgf = pd.read_csv('../data/proteinGroups_failed.txt', sep='\t', low_memory=False)
pgf.to_csv(os.path.join(OUT, 'proteinGroups.txt'), sep='\t', index=False)

g = ev.groupby('Raw file').agg(n=('Sequence', 'size'), tot=('Intensity', 'sum'),
                               med=('Intensity', 'median'))
for c in ('n', 'tot', 'med'):
    g[c + '_rel'] = (g[c] / g[c].median()).round(3)
print(g[['n', 'n_rel', 'tot_rel', 'med_rel']].to_string())
print('\nSKILL.md worked numbers for this failure mode: 0.41x total, 0.62x median')
