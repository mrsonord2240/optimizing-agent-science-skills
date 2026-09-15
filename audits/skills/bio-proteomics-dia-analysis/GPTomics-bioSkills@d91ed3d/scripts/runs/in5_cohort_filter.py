"""Input 5 (Stress) - the Skill's filter/pivot block run AS WRITTEN on the SYNTHETIC 600-run report, timed, plus the
per-run QC and the run-level-vs-global union comparison the user asked for (agent-written around the Skill's code)."""
import os
import time
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, '..'))

t0 = time.perf_counter()
# ---------------- Skill code, verbatim except the path ----------------
report = pd.read_parquet('data/cohort600_report.parquet')  # NOT report.tsv on 1.9+
filt = report[(report['Q.Value'] <= 0.01) &
              (report['PG.Q.Value'] <= 0.01) &
              (report['Global.PG.Q.Value'] <= 0.01)]  # 0.01 = standard 1% FDR
pg = filt.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
pg = np.log2(pg.replace(0, np.nan))  # DIA-NN writes 0 for not-quantified; log2(0) = -Inf
# ----------------------------------------------------------------------
t1 = time.perf_counter()
print(f'rows {len(report):,} | Skill filter+pivot+log2 wall time {t1 - t0:.1f} s | matrix {pg.shape}')
print('-inf cells:', int(np.isinf(pg.to_numpy()).sum()), '| missing', f'{pg.isna().to_numpy().mean():.1%}')
print('FALSE groups in Skill matrix:', int(pg.index.str.startswith('FALSE').sum()))

# Union of accepted groups under a run-level-only protein filter, as the cohort grows
run_only = report[(report['Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.01)]
runs_sorted = sorted(report['Run'].unique())
print('\nN runs | union groups run-level-only | of which FALSE | FALSE share | union groups Skill filter')
for n in (8, 50, 200, 600):
    keep = set(runs_sorted[:n])
    ro = run_only[run_only['Run'].isin(keep)]['Protein.Group'].unique()
    sk = filt[filt['Run'].isin(keep)]['Protein.Group'].unique()
    nf = sum(g.startswith('FALSE') for g in ro)
    print(f'{n:6d} | {len(ro):27d} | {nf:14d} | {nf / len(ro):11.2%} | {len(sk):24d}')

# MBR-context alternative the DIA-NN 1.9.x docs prescribe (Lib.* instead of Global.*)
lib = report[(report['Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.01) &
             (report['Lib.Q.Value'] <= 0.01) & (report['Lib.PG.Q.Value'] <= 0.01)]
print('\nLib.*-based filter (DIA-NN 1.9.x MBR guidance) groups:', lib['Protein.Group'].nunique(),
      '| Skill filter groups:', filt['Protein.Group'].nunique())

# Per-run QC: protein groups per run, flag runs < median - 3 MAD, summarise by batch
ids = pg.notna().sum()
med, mad = ids.median(), (ids - ids.median()).abs().median()
flag = ids[ids < med - 3 * 1.4826 * mad]
by_batch = ids.groupby(ids.index.str[-3:]).median()
print(f'\nper-run protein groups: median {med:.0f}, MAD {mad:.0f}, min {ids.min()}, max {ids.max()}; runs flagged (< median-3*1.4826*MAD): {len(flag)}')
print('median IDs by batch:', by_batch.astype(int).to_dict())
