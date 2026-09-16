# Pass-5 confirmation audit: build a SYNTHETIC TMT10 MaxQuant evidence pair (phospho + global) by
# reshaping this audit's own label-free synthetic set, so data/phospho/truth_sites.csv still applies.
# 8 label-free runs (Ph_C1..C4, Ph_T1..T4 / Gl_*) become 8 reporter channels of one plex, plus two
# pooled reference channels (geometric mean of the 8) carried as Condition = 'Norm'.
# MaxQuant writes TMT10 reporter columns 0-indexed: "Reporter intensity corrected 0" .. " 9".
import os
import numpy as np, pandas as pd

SRC = 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho'
OUT = os.path.dirname(os.path.abspath(__file__)) + '/tmt'
os.makedirs(OUT, exist_ok=True)

KEY = ['Sequence', 'Modified sequence', 'Charge', 'Proteins', 'Leading proteins',
       'Leading razor protein', 'Gene names', 'Protein names', 'Modifications',
       'Phospho (STY) Probabilities', 'Missed cleavages', 'Length', 'Type',
       'Reverse', 'Potential contaminant', 'Protein group IDs']


def reshape(path, prefix, out_name, keep_prob):
    ev = pd.read_csv(path, sep='\t', dtype={'Reverse': str, 'Potential contaminant': str})
    keys = [k for k in KEY if k in ev.columns]
    runs = [f'{prefix}_C{i}' for i in (1, 2, 3, 4)] + [f'{prefix}_T{i}' for i in (1, 2, 3, 4)]
    g = ev.groupby(keys + ['Raw file'], dropna=False)['Intensity'].sum()
    wide = g.unstack('Raw file').reindex(columns=runs)
    # channels 0-7 are the eight biological samples; 8 and 9 are pooled references
    pooled = np.exp(np.log(wide.replace(0, np.nan)).mean(axis=1, skipna=True))
    out = wide.copy()
    out.columns = [f'Reporter intensity corrected {i}' for i in range(8)]
    for i in (8, 9):
        out[f'Reporter intensity corrected {i}'] = pooled * (1.0 + 0.02 * (i - 8))
    out = out.reset_index()
    out['Raw file'] = 'plex1'
    out['Experiment'] = 'plex1'
    out['Intensity'] = out[[f'Reporter intensity corrected {i}' for i in range(10)]].sum(axis=1)
    out['id'] = range(len(out))
    out['PEP'] = 0.001
    out['Score'] = 100.0
    out['Delta score'] = 50.0
    out['m/z'] = 600.0
    out['Retention time'] = 30.0
    out = out.dropna(subset=['Reporter intensity corrected 0'], how='all')
    out.to_csv(f'{OUT}/{out_name}', sep='\t', index=False, na_rep='')
    print(f'{out_name}: {len(out)} precursor rows x 10 channels'
          + (f" | modified rows {(out['Modifications'] != 'Unmodified').sum()}" if keep_prob else ''))
    return out


reshape(f'{SRC}/evidence_phospho.txt', 'Ph', 'evidence_phospho_tmt.txt', True)
reshape(f'{SRC}/evidence_global.txt', 'Gl', 'evidence_global_tmt.txt', False)

for name, bio in (('annotation_ptm_tmt.csv', 'P'), ('annotation_protein_tmt.csv', 'G')):
    for base in (0, 1):
        rows = []
        cond = ['Control'] * 4 + ['Treatment'] * 4 + ['Norm'] * 2
        for i, c in enumerate(cond):
            rows.append(dict(Run='plex1', Fraction=1, TechRepMixture=1,
                             Channel=f'channel.{i + base}', Condition=c, Mixture='mix1',
                             BioReplicate=(f'{bio}{i+1}' if c != 'Norm' else 'Norm')))
        suffix = '' if base == 0 else '_ch1'
        pd.DataFrame(rows).to_csv(f'{OUT}/{name.replace(".csv", suffix + ".csv")}', index=False)

for f in ('proteinGroups_global.txt', 'synthetic.fasta', 'truth_sites.csv'):
    with open(f'{SRC}/{f}', 'rb') as a, open(f'{OUT}/{f}', 'wb') as b:
        b.write(a.read())
print('wrote', sorted(os.listdir(OUT)))
