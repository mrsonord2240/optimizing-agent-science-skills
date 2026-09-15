"""Input 2 (Variant A) - DIA-NN 1.9 report.parquet -> protein x run matrix at 1% FDR.
Part A: the Skill's 'Loading DIA-NN report.parquet' block VERBATIM (path changed only).
Part B: what Claude-with-this-Skill reports (log2, counts).
Part C: AUDITOR checks - LOWCONF leakage (lead 1), PG.MaxLFQ zeros, and the same import with Global.PG.Q.Value.
All data SYNTHETIC (bio-workflows-proteomics-pipeline/data/make_synthetic.py).
"""
import pandas as pd
import numpy as np

PATH = 'F:/OpenScience/audits/bio-proteomics-data-import/data/report.parquet'

# ---------------- Part A: Skill block verbatim ----------------
report = pd.read_parquet(PATH)  # report.tsv dropped as default in DIA-NN 2.0
raw = report.copy()
report = report[(report['Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.01)]  # 1% FDR before quant

matrix = report.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')

# ---------------- Part B: report to user ----------------
print(f'report rows: {len(raw)} | after Q.Value & PG.Q.Value <= 0.01: {len(report)}')
print(f'matrix: {matrix.shape[0]} protein groups x {matrix.shape[1]} runs')
print('valid values per run:', matrix.notna().sum().to_dict())
logm = np.log2(matrix)  # the Skill's DIA block stops at the pivot; log2 is the obvious next step
print('-inf after log2:', int(np.isinf(logm.to_numpy()).sum()))

# ---------------- Part C: auditor checks ----------------
low = matrix.index.str.startswith('LOWCONF')
print('\n[AUDIT] LOWCONF groups in raw report:', raw.loc[raw['Protein.Group'].str.startswith('LOWCONF'), 'Protein.Group'].nunique())
print('[AUDIT] LOWCONF groups surviving the Skill filter into the matrix:', int(low.sum()),
      '| their non-missing cells:', int(matrix[low].notna().sum().sum()),
      '| runs observed per LOWCONF group:', matrix[low].notna().sum(axis=1).value_counts().sort_index().to_dict())
print('[AUDIT] LOWCONF Global.PG.Q.Value values:', sorted(raw.loc[raw['Protein.Group'].str.startswith('LOWCONF'), 'Global.PG.Q.Value'].unique()))
zeros = (matrix == 0)
print('[AUDIT] PG.MaxLFQ == 0 cells carried into the matrix (Skill DIA block has no 0->NaN):', int(zeros.sum().sum()),
      'in', int(zeros.any(axis=1).sum()), 'groups')
# the cross-run filter the dia-analysis Skill prescribes
rep_g = raw[(raw['Q.Value'] <= 0.01) & (raw['PG.Q.Value'] <= 0.01) & (raw['Global.PG.Q.Value'] <= 0.01)]
mat_g = rep_g.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
print('[AUDIT] with Global.PG.Q.Value <= 0.01 added:', mat_g.shape, '| LOWCONF left:', int(mat_g.index.str.startswith('LOWCONF').sum()))
# does a real-target group ever fail Global.PG.Q.Value? (synthetic: all targets pass)
print('[AUDIT] non-LOWCONF groups removed by the global filter:', len(set(matrix.index[~low]) - set(mat_g.index)))
# aggfunc='first' is safe only if PG.MaxLFQ is constant within Protein.Group x Run
nun = report.groupby(['Protein.Group', 'Run'])['PG.MaxLFQ'].nunique().max()
print('[AUDIT] max distinct PG.MaxLFQ within a group x run:', nun)
# 'first' vs pivot_table's NaN-dropping: a group whose every row in a run has NaN quant just disappears for that run
print('[AUDIT] share of LOWCONF among groups observed in <=3 runs:',
      f"{int(low.sum())}/{int((matrix.notna().sum(axis=1) <= 3).sum())}")
