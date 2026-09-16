'''Data-import Input 6 (NEW, edge): MaxQuant TMT10 proteinGroups.txt (no LFQ columns). Block b02 executed verbatim; then the
route its error message suggests; then the agent's reporter-column route. SYNTHETIC data (make_new_tables.py).'''
import os, numpy as np, pandas as pd
os.chdir('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work6')
try:
    with open('../blocks/b02_Loading_and_Cleaning_MaxQuant_proteinGro.py', encoding='utf-8') as fh:
        exec(fh.read(), {})
except ValueError as e:
    print('Skill block ->', 'ValueError:', e)
pg = pd.read_csv('proteinGroups.txt', sep='\t', low_memory=False)
print('Intensity columns per sample available (the suggested fallback):', [c for c in pg.columns if c.startswith('Intensity ')], '| single column:', 'Intensity' in pg.columns)
rep = [c for c in pg.columns if c.startswith('Reporter intensity corrected ')]
mask = (pg.get('Reverse', '') != '+') & (pg.get('Potential contaminant', '') != '+') & (pg.get('Only identified by site', '') != '+')
X = np.log2(pg.loc[mask, rep].replace(0, np.nan)); X.index = pg.loc[mask, 'Protein IDs']
truth = pd.read_csv('truth.csv').set_index('protein')
fc = X.iloc[:, 5:].mean(axis=1) - X.iloc[:, :5].mean(axis=1)
print('agent route: reporter-corrected matrix', X.shape, '| corr(FC, true) =', round(float(np.corrcoef(fc, truth.loc[fc.index, 'true_log2fc'])[0, 1]), 3))
