import pandas as pd
import numpy as np

pg = pd.read_csv('proteinGroups.txt', sep='\t', low_memory=False)  # mixed-type cols

# Flag columns hold '+' or empty string; all three are proteinGroups-only bookkeeping
mask = (pg.get('Reverse', '') != '+') & (pg.get('Potential contaminant', '') != '+') & (pg.get('Only identified by site', '') != '+')
pg = pg[mask].copy()

# Protein IDs / Majority protein IDs / Gene names are SEMICOLON lists; take the first (leading/razor) entry
pg['leading_protein'] = pg['Protein IDs'].str.split(';').str[0]
pg['leading_gene'] = pg['Gene names'].where(pg['Gene names'].notna(), '').str.split(';').str[0]

lfq_cols = [c for c in pg.columns if c.startswith('LFQ intensity ')]  # MaxLFQ-normalized, between-sample comparable
if not lfq_cols:
    raise ValueError('No LFQ intensity columns: LFQ was not enabled in MaxQuant; use Intensity and normalize explicitly')
matrix = pg[['leading_protein', 'leading_gene'] + lfq_cols].copy()
matrix[lfq_cols] = matrix[lfq_cols].replace(0, np.nan)  # MaxQuant writes 0 for missing; log2(0) = -inf
matrix[lfq_cols] = np.log2(matrix[lfq_cols])
matrix = matrix[matrix[lfq_cols].notna().any(axis=1)]  # groups with no valid LFQ value carry no quant
