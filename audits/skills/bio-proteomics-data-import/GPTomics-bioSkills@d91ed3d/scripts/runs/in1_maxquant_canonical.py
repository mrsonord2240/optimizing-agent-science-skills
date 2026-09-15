"""Input 1 (Canonical) - MaxQuant proteinGroups.txt -> clean log2 LFQ matrix.
Part A is the Skill's 'Loading and Cleaning MaxQuant proteinGroups.txt' block VERBATIM (path changed only).
Part B is what Claude-with-this-Skill adds for the user (report counts, save matrix).
Part C is AUDITOR checks (not shown to the user) against the SYNTHETIC generator's known bookkeeping rows.
"""
import pandas as pd
import numpy as np

PATH = 'F:/OpenScience/audits/bio-proteomics-data-import/data/proteinGroups.txt'
print('pandas', pd.__version__, '| numpy', np.__version__)

# ---------------- Part A: Skill block verbatim ----------------
pg = pd.read_csv(PATH, sep='\t', low_memory=False)  # mixed-type cols
raw_pg = pg.copy()

# Flag columns hold '+' or empty string; all three are proteinGroups-only bookkeeping
mask = (pg.get('Reverse', '') != '+') & (pg.get('Potential contaminant', '') != '+') & (pg.get('Only identified by site', '') != '+')
pg = pg[mask].copy()

# Protein IDs / Majority protein IDs / Gene names are SEMICOLON lists; take the first (leading/razor) entry
pg['leading_protein'] = pg['Protein IDs'].str.split(';').str[0]
pg['leading_gene'] = pg['Gene names'].where(pg['Gene names'].notna(), '').str.split(';').str[0]

lfq_cols = [c for c in pg.columns if c.startswith('LFQ intensity ')]  # MaxLFQ-normalized, between-sample comparable
matrix = pg[['leading_protein', 'leading_gene'] + lfq_cols].copy()
matrix[lfq_cols] = matrix[lfq_cols].replace(0, np.nan)  # MaxQuant writes 0 for missing; log2(0) = -inf
matrix[lfq_cols] = np.log2(matrix[lfq_cols])

# ---------------- Part B: report to user ----------------
print(f'rows read: {len(raw_pg)} | kept after flag filter: {len(pg)} | removed: {len(raw_pg) - len(pg)}')
for col in ['Reverse', 'Potential contaminant', 'Only identified by site']:
    print(f'  {col:<24} dtype={raw_pg[col].dtype!s:<8} values={raw_pg[col].value_counts(dropna=False).to_dict()}')
print('LFQ columns:', lfq_cols)
all_missing = matrix[lfq_cols].isna().all(axis=1)
print(f'protein groups with >=1 LFQ value: {(~all_missing).sum()} | all-NaN rows still in matrix: {all_missing.sum()}')
print('-inf present after log2:', bool(np.isinf(matrix[lfq_cols].to_numpy()).any()))
print('per-sample valid values:', matrix[lfq_cols].notna().sum().to_dict())
print(matrix.head(6).to_string(index=False, float_format=lambda v: f'{v:.2f}'))

# ---------------- Part C: auditor checks ----------------
print('\n[AUDIT] surviving REV__/CON__ IDs:', int(matrix['leading_protein'].str.contains('REV__|CON__').sum()))
print('[AUDIT] blank leading_gene:', int((matrix['leading_gene'] == '').sum()),
      '| semicolon genes in raw:', int(pg['Gene names'].fillna('').str.contains(';').sum()),
      '| duplicated leading_gene (non-blank):', int(matrix.loc[matrix.leading_gene != '', 'leading_gene'].duplicated().sum()),
      '| duplicated leading_protein:', int(matrix['leading_protein'].duplicated().sum()))
# peptides >=2 threshold stated in Quantitative Thresholds but not applied in the code block
print('[AUDIT] kept groups with Peptides < 2 (Skill threshold table says >=2, code does not apply it):', int((pg['Peptides'] < 2).sum()))
# a zero-valued flag column scenario: MaxQuant run with no site-only rows -> column all empty -> float64 NaN
t = raw_pg.copy(); t['Only identified by site'] = np.nan
m2 = (t.get('Reverse', '') != '+') & (t.get('Potential contaminant', '') != '+') & (t.get('Only identified by site', '') != '+')
print('[AUDIT] all-empty flag column (float64 NaN) still filters correctly:', int((~m2).sum()), 'rows flagged (expect 45)')
# missing flag column entirely (e.g. evidence.txt has no Only identified by site)
t2 = raw_pg.drop(columns=['Only identified by site'])
m3 = (t2.get('Reverse', '') != '+') & (t2.get('Potential contaminant', '') != '+') & (t2.get('Only identified by site', '') != '+')
print('[AUDIT] missing flag column handled by .get default:', int((~m3).sum()), 'rows flagged (expect 45)')
matrix.to_csv('F:/OpenScience/audits/bio-proteomics-data-import/runs/in1_lfq_log2_matrix.tsv', sep='\t', index=False)
