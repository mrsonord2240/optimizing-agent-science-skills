"""SYNTHETIC 3-arm LFQ protein matrix for the bio-proteomics-differential-abundance audit (2026-09-11).
NOT REAL DATA. Control / DrugA / DrugB, 4 replicates each, acquired over 3 days (unbalanced:
D1 = C1 C2 A1 B1, D2 = C3 A2 A3 B2, D3 = C4 A4 B3 B4), day effect protein-specific (mean +0.25 / -0.2).
1200 proteins; DrugA vs Control: 100 changed, half 'small' (|log2FC| 0.15-0.5) and half 'large' (0.7-2.0);
DrugB vs Control: 70 changed (0.15-2.0). Replicate SD depends on intensity (0.25 at high, ~0.6 at low
abundance). Left-censored detection (logistic around 21.5, scale 0.5) + 2% MCAR.
Writes three_arm_log2.csv (log2, NA = missing), three_arm_samples.csv, three_arm_truth.csv.
"""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(3303)
NP = 1200
prot = [f'TA{i:04d}' for i in range(NP)]
base = rng.normal(24.5, 2.0, NP)
fcA = np.zeros(NP); fcB = np.zeros(NP)
p = rng.permutation(NP)
fcA[p[:50]] = rng.choice([-1, 1], 50) * rng.uniform(0.15, 0.5, 50)
fcA[p[50:100]] = rng.choice([-1, 1], 50) * rng.uniform(0.7, 2.0, 50)
q = rng.permutation(NP)[:70]
fcB[q] = rng.choice([-1, 1], 70) * rng.uniform(0.15, 2.0, 70)
samples = pd.DataFrame({
    'sample': ['C1', 'C2', 'C3', 'C4', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4'],
    'condition': ['Control'] * 4 + ['DrugA'] * 4 + ['DrugB'] * 4,
    'batch': ['D1', 'D1', 'D2', 'D3', 'D1', 'D2', 'D2', 'D3', 'D1', 'D2', 'D3', 'D3']})
day = {'D1': np.zeros(NP), 'D2': rng.normal(0.25, 0.2, NP), 'D3': rng.normal(-0.2, 0.2, NP)}
sd = 0.25 + 0.35 / (1 + np.exp((base - 22.5) / 0.8))
mat = np.empty((NP, 12))
for j, r in samples.iterrows():
    eff = fcA if r.condition == 'DrugA' else (fcB if r.condition == 'DrugB' else 0)
    x = base + eff + day[r.batch] + rng.normal(0, sd) + rng.normal(0, 0.1)
    seen = (rng.random(NP) < 1 / (1 + np.exp(-(x - 21.5) / 0.5))) & (rng.random(NP) > 0.02)
    mat[:, j] = np.where(seen, x, np.nan)
pd.DataFrame(mat.round(4), index=pd.Index(prot, name='protein'), columns=samples['sample']).to_csv(os.path.join(OUT, 'three_arm_log2.csv'))
samples.to_csv(os.path.join(OUT, 'three_arm_samples.csv'), index=False)
pd.DataFrame({'protein': prot, 'fc_DrugA': fcA, 'fc_DrugB': fcB}).to_csv(os.path.join(OUT, 'three_arm_truth.csv'), index=False)
print('missing', np.isnan(mat).mean().round(3), '| all-NA rows', int(np.isnan(mat).all(1).sum()))
