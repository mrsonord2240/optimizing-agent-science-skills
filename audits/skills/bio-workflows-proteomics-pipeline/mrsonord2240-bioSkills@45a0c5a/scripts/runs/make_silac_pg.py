'''SYNTHETIC MaxQuant SILAC proteinGroups.txt for pipeline Input 7 (2026-09-15): 3 replicates, "Ratio H/L normalized <rep>",
NaN where MaxQuant could not form a ratio (on/off or low-abundance). NOT REAL DATA.'''
import numpy as np, pandas as pd
rng = np.random.default_rng(97); n = 500
eff = np.zeros(n); eff[:50] = rng.choice([-1.5, 1.5], 50)
d = pd.DataFrame({'Protein IDs': [f'S{i:04d}' for i in range(n)], 'Reverse': '', 'Potential contaminant': '', 'Only identified by site': ''})
for r in ['rep1', 'rep2', 'rep3']:
    x = 2 ** (eff + rng.normal(0, 0.3, n)); x[rng.random(n) < 0.12] = np.nan; d[f'Ratio H/L normalized {r}'] = x
d.loc[50:59, [f'Ratio H/L normalized rep{k}' for k in (2, 3)]] = np.nan   # 10 proteins with a single ratio
d.to_csv('F:/OpenScience/audits/bio-workflows-proteomics-pipeline/runs/work7/proteinGroups.txt', sep='\t', index=False)
pd.DataFrame({'protein': d['Protein IDs'], 'true_log2fc': eff}).to_csv('F:/OpenScience/audits/bio-workflows-proteomics-pipeline/runs/work7/truth.csv', index=False)
print('written; rows with <2 ratios:', int((d.filter(like='Ratio').notna().sum(axis=1) < 2).sum()))
