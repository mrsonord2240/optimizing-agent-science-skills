"""Auditor edge check: MaxQuant run with LFQ disabled (no 'LFQ intensity' columns) through the Skill's MaxQuant block."""
import pandas as pd, numpy as np
pg = pd.read_csv('F:/OpenScience/audits/bio-proteomics-data-import/data/proteinGroups.txt', sep='\t', low_memory=False)
pg = pg.drop(columns=[c for c in pg.columns if c.startswith('LFQ intensity ')])
mask = (pg.get('Reverse', '') != '+') & (pg.get('Potential contaminant', '') != '+') & (pg.get('Only identified by site', '') != '+')
pg = pg[mask].copy()
pg['leading_protein'] = pg['Protein IDs'].str.split(';').str[0]
pg['leading_gene'] = pg['Gene names'].where(pg['Gene names'].notna(), '').str.split(';').str[0]
lfq_cols = [c for c in pg.columns if c.startswith('LFQ intensity ')]
matrix = pg[['leading_protein', 'leading_gene'] + lfq_cols].copy()
matrix[lfq_cols] = matrix[lfq_cols].replace(0, np.nan)
matrix[lfq_cols] = np.log2(matrix[lfq_cols])
print('no error raised; matrix shape', matrix.shape, 'columns', list(matrix.columns))
