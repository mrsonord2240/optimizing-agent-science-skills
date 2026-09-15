"""Input 5 (Stress) - SYNTHETIC 600-run DIA-NN-style long report (NOT real data; seeded).

Model (constructed to exercise the Skill's cohort-FDR claim, not a proof of it):
  * 2000 true protein groups, 3 precursors each, detection probability by abundance (left-censored), 12 batches of 50 runs.
    Run-level Q.Value / PG.Q.Value and experiment-wide Global.* / Lib.* q-values all small (<= 0.005).
  * 2000 false candidate groups ('FALSE####'): in any run a false group appears in the report (its precursor passed the
    run-level --qvalue 0.01 cut) with probability 0.03; its run-level PG.Q.Value ~ U(0, 0.3), so it passes a run-level
    1% protein filter in a given run with probability ~0.001; its experiment-wide Global.PG.Q.Value / Lib.PG.Q.Value is
    U(0.02, 0.5) (fails a global 1% filter).
  * PG.MaxLFQ: ~1% zeros (DIA-NN 'not quantified').
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'cohort600_report.parquet')
rng = np.random.default_rng(20260911)

N_RUNS, N_TRUE, N_FALSE, N_PREC = 600, 2000, 2000, 3
runs = np.array([f'P{r:03d}_B{r // 50 + 1:02d}' for r in range(N_RUNS)])
base = rng.normal(24, 2.2, N_TRUE)
batch_shift = rng.normal(0, 0.3, 12)

frames = []
for r in range(N_RUNS):
    b = r // 50
    x = base + batch_shift[b] + rng.normal(0, 0.4, N_TRUE)
    seen = rng.random(N_TRUE) < 1 / (1 + np.exp(-(x - 21.5) / 0.6))
    idx = np.where(seen)[0]
    k = len(idx)
    maxlfq = np.where(rng.random(k) < 0.01, 0.0, np.round(2 ** x[idx], 1))
    df = pd.DataFrame({
        'Run': runs[r],
        'Protein.Group': np.char.add('TRUE', np.char.zfill(idx.astype(str), 4)),
        'PG.Q.Value': 10 ** rng.uniform(-5, -2.3, k),
        'Global.PG.Q.Value': 10 ** rng.uniform(-5, -2.3, k),
        'Lib.PG.Q.Value': 10 ** rng.uniform(-5, -2.3, k),
        'PG.MaxLFQ': maxlfq,
    })
    df = df.loc[df.index.repeat(N_PREC)].reset_index(drop=True)
    n = len(df)
    df['Precursor.Id'] = df['Protein.Group'] + '_p' + np.tile(np.arange(N_PREC), k).astype(str)
    df['Q.Value'] = 10 ** rng.uniform(-5, -2, n)
    df['Global.Q.Value'] = 10 ** rng.uniform(-5, -2.2, n)
    df['Lib.Q.Value'] = 10 ** rng.uniform(-5, -2.2, n)
    # false candidates present in this run
    fidx = np.where(rng.random(N_FALSE) < 0.03)[0]
    m = len(fidx)
    fdf = pd.DataFrame({
        'Run': runs[r],
        'Protein.Group': np.char.add('FALSE', np.char.zfill(fidx.astype(str), 4)),
        'PG.Q.Value': rng.uniform(0, 0.3, m),
        'Global.PG.Q.Value': rng.uniform(0.02, 0.5, m),
        'Lib.PG.Q.Value': rng.uniform(0.02, 0.5, m),
        'PG.MaxLFQ': np.round(2 ** rng.normal(19.5, 0.8, m), 1),
    })
    fdf['Precursor.Id'] = fdf['Protein.Group'] + '_p0'
    fdf['Q.Value'] = rng.uniform(0.0005, 0.01, m)
    fdf['Global.Q.Value'] = rng.uniform(0.01, 0.2, m)
    fdf['Lib.Q.Value'] = rng.uniform(0.01, 0.2, m)
    frames.append(df)
    frames.append(fdf)

report = pd.concat(frames, ignore_index=True)
report.to_parquet(OUT, index=False)
print('SYNTHETIC cohort report written:', OUT, '| rows', len(report), '| runs', report['Run'].nunique(),
      '| groups', report['Protein.Group'].nunique(), '| MB', round(os.path.getsize(OUT) / 1e6, 1))
