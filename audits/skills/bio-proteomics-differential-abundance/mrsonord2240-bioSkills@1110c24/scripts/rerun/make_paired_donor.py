'''SYNTHETIC paired-donor LFQ protein matrix for re-audit Input 8 (2026-09-15). NOT REAL DATA.
6 donors x (unstimulated, LPS) = 12 samples. 1000 proteins; 80 changed (|log2FC| 0.5-1.5); donor effect SD 0.6 per
protein x donor (large relative to replicate noise SD 0.25), so pairing matters. Left-censored dropout (logistic
around log2 21) + 2% MCAR. Peptide counts ~ geometric, larger for abundant proteins.
'''
import numpy as np
import pandas as pd
rng = np.random.default_rng(915)
NP, donors = 1000, [f'D{i}' for i in range(1, 7)]
prot = [f'PD{i:04d}' for i in range(NP)]
eff = np.zeros(NP)
idx = rng.permutation(NP)[:80]
eff[idx[:40]] = rng.uniform(0.5, 1.5, 40)
eff[idx[40:]] = -rng.uniform(0.5, 1.5, 40)
base = rng.normal(23.5, 2.0, NP)
donor_eff = {d: rng.normal(0, 0.6, NP) for d in donors}
cols, info = {}, []
for d in donors:
    for c in ('Unstim', 'LPS'):
        x = base + donor_eff[d] + (eff if c == 'LPS' else 0) + rng.normal(0, 0.25, NP)
        p_detect = 1 / (1 + np.exp(-(x - 21.0) * 2.5))
        x[(rng.random(NP) > p_detect) | (rng.random(NP) < 0.02)] = np.nan
        cols[f'{d}_{c}'] = x
        info.append({'sample': f'{d}_{c}', 'condition': c, 'donor': d})
out = 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data/'
pd.DataFrame(cols, index=pd.Index(prot, name='protein')).round(4).to_csv(out + 'paired_donor_log2.csv')
pd.DataFrame(info).to_csv(out + 'paired_donor_samples.csv', index=False)
pep = np.maximum(1, rng.geometric(1 / np.clip(np.exp((base - 20) / 2.5), 1.2, 25)))
pd.DataFrame({'protein': prot, 'true_log2fc': eff, 'class': np.where(eff > 0, 'up', np.where(eff < 0, 'down', 'null')),
              'peptides': pep}).to_csv(out + 'paired_donor_truth.csv', index=False)
print('written', NP, 'proteins; missing %', round(100 * np.isnan(pd.DataFrame(cols).values).mean(), 1))
