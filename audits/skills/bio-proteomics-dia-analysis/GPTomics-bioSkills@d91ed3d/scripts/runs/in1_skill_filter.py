"""Input 1/2 - the Skill's 'DIA-NN Output and Correct Filtering' block, run AS WRITTEN (only the path changed:
'diann_out/report.parquet' -> the SYNTHETIC shared report copied to ../data/report.parquet), followed by audit checks.
"""
import os
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, '..'))

# ---------------- Skill code, verbatim except the path ----------------
report = pd.read_parquet('data/report.parquet')  # NOT report.tsv on 1.9+

# Per-run filter: both LEVELS. Add Global.PG.Q.Value for the cross-run matrix.
filt = report[(report['Q.Value'] <= 0.01) &
              (report['PG.Q.Value'] <= 0.01) &
              (report['Global.PG.Q.Value'] <= 0.01)]  # 0.01 = standard 1% FDR

# Pivot to a protein matrix from the filtered long report.
pg = filt.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
pg = np.log2(pg.replace(0, np.nan))  # DIA-NN writes 0 for not-quantified; log2(0) = -Inf
# ----------------------------------------------------------------------

print('report rows', len(report), '| runs', report['Run'].nunique(), '| protein groups', report['Protein.Group'].nunique())
print('filtered rows (Skill filter)', len(filt))
print('Skill matrix shape', pg.shape)
low = pg.index.str.startswith('LOWCONF')
print('LOWCONF groups in report:', report.loc[report['Protein.Group'].str.startswith('LOWCONF'), 'Protein.Group'].nunique())
print('LOWCONF groups surviving Skill filter:', int(low.sum()))

# Audit comparison 1: run-level-only filter (the pattern the Skill warns against for cohorts)
run_only = report[(report['Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.01)]
pg_run = run_only.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
print('run-level-only matrix shape', pg_run.shape,
      '| LOWCONF surviving run-level-only:', int(pg_run.index.str.startswith('LOWCONF').sum()))

# Audit comparison 2: DIA-NN README (master, 2.6.1) recommended set: Q.Value, Global.Q.Value, Global.PG.Q.Value at 0.01,
# PG.Q.Value 0.05
readme = report[(report['Q.Value'] <= 0.01) & (report['Global.Q.Value'] <= 0.01) &
                (report['Global.PG.Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.05)]
print('README-recommended filter matrix groups', readme['Protein.Group'].nunique())

# Audit checks on 0 -> NaN -> log2
raw_pivot = filt.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
print('zeros in PG.MaxLFQ (report rows):', int((report['PG.MaxLFQ'] == 0).sum()),
      f"({(report['PG.MaxLFQ'] == 0).mean():.2%})")
print('zeros in pivoted matrix before replace:', int((raw_pivot == 0).sum().sum()))
print('-inf in Skill log2 matrix:', int(np.isinf(pg.to_numpy()).sum()), '| NaN cells:', int(pg.isna().sum().sum()),
      f'({pg.isna().to_numpy().mean():.1%} missing)')
# Is PG.MaxLFQ constant within (group, run)? aggfunc='first' is only safe if so
nuniq = filt.groupby(['Protein.Group', 'Run'])['PG.MaxLFQ'].nunique()
print('max distinct PG.MaxLFQ per (group, run):', int(nuniq.max()))
# Precursor-level rows failing Q.Value but group still present via other precursors
print('precursor rows removed by Q.Value<=0.01 alone:', int((report['Q.Value'] > 0.01).sum()))
print('per-run protein counts (Skill matrix):')
print(pg.notna().sum().to_string())
print('matrix head:')
print(pg.iloc[:4].round(2).to_string())
pg.to_csv('runs/in1_pg_log2_matrix.tsv', sep='\t')
