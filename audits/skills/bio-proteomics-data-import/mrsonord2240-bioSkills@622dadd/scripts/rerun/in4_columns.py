'''Data-import Input 4 (regression): Intensity vs iBAQ vs LFQ intensity for treated vs control, one weak run (T4). SYNTHETIC
proteinGroups_failed.txt. The Skill's cleaning pattern (b02 logic) applied per column family.'''
import numpy as np, pandas as pd
D = 'F:/OpenScience/audits/bio-proteomics-data-import/data/'
pg = pd.read_csv(D + 'proteinGroups_failed.txt', sep='\t', low_memory=False)
mask = (pg.get('Reverse', '') != '+') & (pg.get('Potential contaminant', '') != '+') & (pg.get('Only identified by site', '') != '+')
pg = pg[mask].copy(); pg['leading_protein'] = pg['Protein IDs'].str.split(';').str[0]
truth = pd.read_csv(D + 'truth_proteins.csv', keep_default_na=False).set_index('protein')   # 'null' must stay a string under pandas 3
S = ['C1', 'C2', 'C3', 'C4', 'T1', 'T2', 'T3', 'T4']
mats = {fam: np.log2(pg.set_index('leading_protein')[[f'{fam} {s}' for s in S]].replace(0, np.nan)).set_axis(S, axis=1) for fam in ['Intensity', 'iBAQ', 'LFQ intensity']}
cc = set.intersection(*[set(m.dropna().index) for m in mats.values()])
nulls = [p for p in cc if truth.loc[p, 'class'] == 'null']
print('complete-case proteins:', len(cc), '| true nulls among them:', len(nulls))
for fam, m in mats.items():
    mm = m.loc[sorted(cc)]
    t4 = float(np.median(mm['T4'] - mm.drop(columns='T4').mean(axis=1)))
    nfc = float(np.median(mm.loc[nulls, ['T1', 'T2', 'T3', 'T4']].mean(axis=1) - mm.loc[nulls, ['C1', 'C2', 'C3', 'C4']].mean(axis=1)))
    print(f'{fam:14s} T4 - mean(other runs) median {t4:+.2f} | true-null median T/C log2FC {nfc:+.3f} | valid T4 {int(m["T4"].notna().sum())}')
r = (mats['iBAQ'] - mats['Intensity']).loc[sorted(cc)]
print('max within-protein SD of log2(iBAQ/Intensity) across samples:', round(float(r.std(axis=1).max()), 6))
