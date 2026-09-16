'''SYNTHETIC tables for data-import re-audit Inputs 6-7 (2026-09-15). NOT REAL DATA.
work6/proteinGroups.txt: MaxQuant 2.x TMT10 run (one experiment, 10 reporter channels: 5 ctrl, 5 treated), no LFQ columns.
work7/combined_protein.tsv: FragPipe 20-style IonQuant output, 6 samples, contam_ prefixed contaminants, MaxLFQ + raw Intensity.'''
import numpy as np, pandas as pd
rng = np.random.default_rng(915)
n = 400
ids = [f'P{i:05d}' for i in range(n)]
base = rng.normal(22, 2, n); eff = np.zeros(n); eff[:40] = rng.choice([-1.2, 1.2], 40)
pg = pd.DataFrame({'Protein IDs': ids, 'Majority protein IDs': ids, 'Gene names': [f'G{i}' for i in range(n)],
                   'Peptides': rng.integers(1, 20, n), 'Razor + unique peptides': rng.integers(1, 20, n),
                   'Reverse': '', 'Potential contaminant': '', 'Only identified by site': ''})
pg.loc[n - 10:n - 6, 'Reverse'] = '+'; pg.loc[n - 5:, 'Potential contaminant'] = '+'
chan = {}
for k in range(1, 11):
    x = base + (eff * 0.7 if k > 5 else 0) + rng.normal(0, 0.2, n)
    chan[f'Reporter intensity corrected {k}'] = np.round(2 ** x, 1)
    chan[f'Reporter intensity {k}'] = np.round(2 ** (x + 0.02), 1)
pg = pd.concat([pg, pd.DataFrame(chan)], axis=1)
pg['Intensity'] = np.round(pg[[f'Reporter intensity {k}' for k in range(1, 11)]].sum(axis=1) * 3, 1)
pg.to_csv('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work6/proteinGroups.txt', sep='\t', index=False)
pd.DataFrame({'protein': ids, 'true_log2fc': eff}).to_csv('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work6/truth.csv', index=False)
m = 300
prot = [f'sp|Q{i:05d}|PROT{i}_HUMAN' for i in range(m)]
prot[-8:] = [f'contam_sp|P{i:05d}|K2C1_HUMAN' for i in range(8)]
fp = pd.DataFrame({'Protein': prot, 'Protein ID': [p.split('|')[1] for p in prot], 'Entry Name': [p.split('|')[2] for p in prot],
                   'Gene': [f'PROT{i}' for i in range(m)], 'Protein Probability': 1.0, 'Indistinguishable Proteins': ''})
for s in ['ctrl_1', 'ctrl_2', 'ctrl_3', 'trt_1', 'trt_2', 'trt_3']:
    x = rng.normal(24, 2, m); x[rng.random(m) < 0.15] = np.nan
    fp[f'{s} Spectral Count'] = rng.integers(0, 30, m)
    fp[f'{s} Intensity'] = np.where(np.isnan(x), 0, np.round(2 ** (x + 0.3), 1))
    fp[f'{s} MaxLFQ Intensity'] = np.where(np.isnan(x), 0, np.round(2 ** x, 1))
fp.to_csv('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work7/combined_protein.tsv', sep='\t', index=False)
print('written')
