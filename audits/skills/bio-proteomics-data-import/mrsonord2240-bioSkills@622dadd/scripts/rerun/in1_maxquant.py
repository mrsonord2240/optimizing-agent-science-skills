'''Data-import Input 1 (regression): MaxQuant 2.x proteinGroups.txt, 8 LFQ runs -> clean log2 LFQ matrix. SYNTHETIC data.
SKILL.md block b02 executed verbatim (cwd = rerun/work, which holds a copy of proteinGroups.txt).'''
import os, warnings, numpy as np, pandas as pd
os.chdir('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work')
warnings.simplefilter('always')
ns = {}
with warnings.catch_warnings(record=True) as w:
    with open('../blocks/b02_Loading_and_Cleaning_MaxQuant_proteinGro.py', encoding='utf-8') as fh:
        exec(fh.read(), ns)
    print('warnings:', [str(x.message) for x in w])
raw, pg, m, lfq = pd.read_csv('proteinGroups.txt', sep='\t', low_memory=False), ns['pg'], ns['matrix'], ns['lfq_cols']
print(f'rows read {len(raw)} | kept after flag filter {len(pg)} | final matrix {m.shape} | all-NaN rows {int(m[lfq].isna().all(axis=1).sum())} | -inf {int(np.isinf(m[lfq].values).sum())}')
print('surviving REV__/CON__ IDs:', int(m['leading_protein'].str.startswith(('REV__', 'CON__')).sum()), '| blank leading_gene:', int((m['leading_gene'] == '').sum()))
print('groups with Razor + unique peptides < 2 still in matrix (threshold is documented as not applied):',
      int((pg.loc[m.index, 'Razor + unique peptides'] < 2).sum()))
# edge: table without LFQ columns -> the new ValueError
nl = raw.drop(columns=[c for c in raw.columns if c.startswith('LFQ intensity ')]); nl.to_csv('proteinGroups.txt', sep='\t', index=False)
try:
    with open('../blocks/b02_Loading_and_Cleaning_MaxQuant_proteinGro.py', encoding='utf-8') as fh:
        exec(fh.read(), {})
except ValueError as e:
    print('no-LFQ table ->', 'ValueError:', e)
raw.to_csv('proteinGroups.txt', sep='\t', index=False)
