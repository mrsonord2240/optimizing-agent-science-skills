"""Input 4 (Variant B) - "Intensity vs iBAQ vs LFQ intensity: which one, and why?" on proteinGroups_failed.txt
(SYNTHETIC: T4 loaded ~3x low; MaxLFQ re-normalised T4's LFQ column, residual -0.2 log2).
Uses the Skill's cleaning block (verbatim mask / 0->NaN / log2) applied to each of the three column families,
then reports what the Decision Tree predicts: raw Intensity/iBAQ track loading, LFQ does not.
"""
import pandas as pd
import numpy as np

PATH = 'F:/OpenScience/audits/bio-proteomics-data-import/data/proteinGroups_failed.txt'
pg = pd.read_csv(PATH, sep='\t', low_memory=False)
mask = (pg.get('Reverse', '') != '+') & (pg.get('Potential contaminant', '') != '+') & (pg.get('Only identified by site', '') != '+')
pg = pg[mask].copy()
pg['leading_protein'] = pg['Protein IDs'].str.split(';').str[0]

samples = ['C1', 'C2', 'C3', 'C4', 'T1', 'T2', 'T3', 'T4']
fam = {'Intensity': [f'Intensity {s}' for s in samples],
       'iBAQ': [f'iBAQ {s}' for s in samples],
       'LFQ intensity': [f'LFQ intensity {s}' for s in samples]}
truth = pd.read_csv('F:/OpenScience/audits/bio-proteomics-data-import/data/truth_proteins.csv', keep_default_na=False)  # 'null' is a class label
null = set(truth.loc[truth['class'] == 'null', 'protein'])

logs = {name: np.log2(pg[cols].replace(0, np.nan)) for name, cols in fam.items()}
complete = np.logical_and.reduce([logs[k].notna().all(axis=1).to_numpy() for k in logs])  # same proteins for all 3 columns
print('complete-case proteins (valid in all 8 runs for all 3 columns):', int(complete.sum()))
print(f'{"column":<14}{"median log2 of complete cases (C1..T4)":<62}{"T4 - median(others)":>20}{"null-protein median T/C log2FC":>32}{"valid T4":>10}')
for name, cols in fam.items():
    m = logs[name]
    med = m[complete].median()
    t4_shift = med.iloc[7] - med.iloc[:7].median()
    lfc = m[cols[4:]].mean(axis=1) - m[cols[:4]].mean(axis=1)
    lfc_null = lfc[complete & pg['leading_protein'].isin(null).to_numpy()].median()
    print(f'{name:<14}{" ".join(f"{v:6.2f}" for v in med):<62}{t4_shift:>20.2f}{lfc_null:>32.3f}{int(m[cols[7]].notna().sum()):>10}')
# T4 residual vs others on the SAME proteins, per column (the loading artefact the Decision Tree warns about)
for name, cols in fam.items():
    m = logs[name][complete]
    d = (m[cols[7]] - m[cols[:7]].mean(axis=1)).median()
    print(f'  {name:<14} per-protein median (T4 - mean of other 7 runs) = {d:+.2f} log2')

# iBAQ within-sample use: rank proteins by molar share in one sample
ib = pg[fam['iBAQ'][0]].replace(0, np.nan)
share = (ib / ib.sum() * 100).sort_values(ascending=False)
print('\nTop-3 proteins by iBAQ molar share in C1 (%):',
      ', '.join(f'{pg.loc[i, "leading_protein"]} {v:.2f}' for i, v in share.head(3).items()))
# Intensity vs iBAQ give the same between-sample ratios (iBAQ = Intensity / n_theoretical_peptides, constant per protein)
r = (np.log2(pg[fam['iBAQ']].replace(0, np.nan)).sub(np.log2(pg[fam['Intensity']].replace(0, np.nan)).to_numpy())).std(axis=1).max()
print('max within-protein SD of log2(iBAQ/Intensity) across samples:', round(float(r), 6))
