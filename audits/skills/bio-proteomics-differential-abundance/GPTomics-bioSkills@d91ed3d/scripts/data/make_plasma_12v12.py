"""SYNTHETIC 12-vs-12 plasma protein matrix for the bio-proteomics-differential-abundance audit (2026-09-11).
NOT REAL DATA. 900 proteins, wide dynamic range (log2 12-32), 70 truly changed (|log2FC| 0.4-1.2),
8 'on/off' proteins absent in every case sample, per-sample loading offsets (SD 0.3, two samples -0.8),
between-subject SD 0.45 log2, left-censored detection (logistic around log2 17) + 1% MCAR.
Writes plasma_12v12.csv (protein x sample raw intensities, NaN = not detected) and plasma_truth.csv.
"""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(1212)
NP = 900
prot = [f'PL{i:04d}' for i in range(NP)]
base = np.clip(rng.gamma(6, 3.2, NP) + 7, 12, 32)
eff = np.zeros(NP)
cls = np.array(['null'] * NP, dtype=object)
perm = rng.permutation(NP)
up, dn, oo = perm[:35], perm[35:70], perm[70:78]
eff[up] = rng.uniform(0.4, 1.2, 35); cls[up] = 'up'
eff[dn] = -rng.uniform(0.4, 1.2, 35); cls[dn] = 'down'
cls[oo] = 'on_off'
base[oo] = rng.uniform(19, 24, 8)
cols = [f'ctrl_{i+1:02d}' for i in range(12)] + [f'case_{i+1:02d}' for i in range(12)]
load = rng.normal(0, 0.3, 24); load[[3, 17]] -= 0.8
mat = np.empty((NP, 24))
for j, c in enumerate(cols):
    is_case = c.startswith('case')
    x = base + (eff if is_case else 0) + rng.normal(0, 0.45, NP) + load[j]
    p_det = 1 / (1 + np.exp(-(x - 17) / 0.6))
    seen = (rng.random(NP) < p_det) & (rng.random(NP) > 0.01)
    if is_case:
        seen[oo] = False
    mat[:, j] = np.where(seen, 2 ** x, np.nan)
pd.DataFrame(mat, index=pd.Index(prot, name='protein'), columns=cols).round(1).to_csv(os.path.join(OUT, 'plasma_12v12.csv'))
pd.DataFrame({'protein': prot, 'class': cls, 'true_log2fc': eff}).to_csv(os.path.join(OUT, 'plasma_truth.csv'), index=False)
print('missing fraction', np.isnan(mat).mean().round(3))
