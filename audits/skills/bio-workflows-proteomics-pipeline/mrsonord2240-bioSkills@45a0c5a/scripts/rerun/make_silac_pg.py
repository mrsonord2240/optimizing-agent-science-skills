"""SYNTHETIC MaxQuant SILAC proteinGroups.txt for the re-audit of bio-workflows-proteomics-pipeline
(2026-09-15). 3 replicates, 'Ratio H/L normalized <rep>', NaN where MaxQuant could not form a ratio,
0 where a channel is absent. Includes 'Majority protein IDs' as a real MaxQuant table does.
NOT REAL DATA. Independent seed from the pre-fix audit's generator."""
import numpy as np, pandas as pd
OUT = 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline/rerun/work7'
rng = np.random.default_rng(20260915); n = 500
eff = np.zeros(n); eff[:50] = rng.choice([-1.5, 1.5], 50)
ids = [f'S{i:04d}' for i in range(n)]
d = pd.DataFrame({'Protein IDs': ids, 'Majority protein IDs': ids,
                  'Reverse': '', 'Potential contaminant': '', 'Only identified by site': ''})
for r in ('rep1', 'rep2', 'rep3'):
    x = 2 ** (eff + rng.normal(0, 0.3, n))
    x[rng.random(n) < 0.12] = np.nan
    d[f'Ratio H/L normalized {r}'] = x
# 30 proteins quantified in one replicate only -> the case that stopped the pre-fix block
d.loc[50:79, ['Ratio H/L normalized rep2', 'Ratio H/L normalized rep3']] = np.nan
# 15 proteins with an absent channel -> MaxQuant writes 0, log2 gives -Inf
d.loc[80:94, 'Ratio H/L normalized rep1'] = 0.0
d.to_csv(f'{OUT}/proteinGroups.txt', sep='\t', index=False)
pd.DataFrame({'protein': ids, 'true_log2fc': eff}).to_csv(f'{OUT}/truth.csv', index=False)
rc = d.filter(like='Ratio')
print('rows:', n, '| rows with <2 finite ratios:', int(((rc.notna() & (rc != 0)).sum(axis=1) < 2).sum()),
      '| true changers:', int((eff != 0).sum()))
