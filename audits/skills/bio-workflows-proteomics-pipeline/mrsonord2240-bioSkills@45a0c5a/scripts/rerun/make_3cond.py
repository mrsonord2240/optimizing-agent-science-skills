"""Re-audit new Input C: SYNTHETIC MaxQuant proteinGroups.txt for a THREE-condition dose design
(Control / LowDose / HighDose, n=4 each, two batches) to test whether the Skill's Complete R Workflow
block generalizes past its hard-coded two-level Treatment - Control contrast. NOT REAL DATA."""
import numpy as np, pandas as pd
OUT = 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline/rerun/workC'
rng = np.random.default_rng(31415); n = 1200
samples = [f'{c}{i}' for c in ('Ctl', 'Low', 'High') for i in (1, 2, 3, 4)]
cond = {s: s[:-1] for s in samples}
batch = {s: ('B1' if s[-1] in '12' else 'B2') for s in samples}
base = rng.normal(26, 1.6, n)
cls = np.array(['null'] * n, dtype=object)
cls[:60] = 'dose_up'; cls[60:120] = 'dose_down'; cls[120:150] = 'high_only'
eff = {'Ctl': np.zeros(n), 'Low': np.zeros(n), 'High': np.zeros(n)}
eff['Low'][:60] = 0.7;  eff['High'][:60] = 1.4
eff['Low'][60:120] = -0.7; eff['High'][60:120] = -1.4
eff['High'][120:150] = 1.6
bshift = {'B1': 0.0, 'B2': 0.35}
d = pd.DataFrame({'Protein IDs': [f'P{i:05d}' for i in range(n)],
                  'Majority protein IDs': [f'P{i:05d}' for i in range(n)],
                  'Only identified by site': '', 'Reverse': '', 'Potential contaminant': ''})
mat = {}
for s in samples:
    v = base + eff[cond[s]] + bshift[batch[s]] + rng.normal(0, 0.35, n)
    lin = 2 ** v
    miss = rng.random(n) < np.clip(0.55 - 0.018 * (v - v.min()), 0.02, 0.6)  # MNAR: low -> missing
    lin[miss] = 0.0
    mat[s] = lin
for pre in ('Intensity', 'LFQ intensity'):
    for s in samples:
        d[f'{pre} {s}'] = mat[s]
d.to_csv(f'{OUT}/proteinGroups.txt', sep='\t', index=False)
pd.DataFrame({'sample': samples, 'condition': [cond[s] for s in samples],
              'replicate': [s[-1] for s in samples], 'batch': [batch[s] for s in samples]}
             ).to_csv(f'{OUT}/sample_annotation.csv', index=False)
pd.DataFrame({'protein': d['Protein IDs'], 'class': cls}).to_csv(f'{OUT}/truth.csv', index=False)
print('written: 3 conditions x 4 =', len(samples), 'samples,', n, 'proteins;',
      'dose_up 60, dose_down 60, high_only 30, null', int((cls == 'null').sum()))
