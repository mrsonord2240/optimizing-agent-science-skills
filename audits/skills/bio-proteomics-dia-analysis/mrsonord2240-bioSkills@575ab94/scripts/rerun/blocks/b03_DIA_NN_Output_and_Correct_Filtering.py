import pandas as pd, numpy as np
report = pd.read_parquet('diann_out/report.parquet')  # NOT report.tsv on 1.9+

# Run-level LEVELS (Q.Value, PG.Q.Value) plus experiment-wide CONTEXT (Global.Q.Value, Global.PG.Q.Value) for a
# cross-run matrix. DIA-NN 1.9.x with MBR: use Lib.Q.Value / Lib.PG.Q.Value instead of the Global.* pair.
filt = report[(report['Q.Value'] <= 0.01) &
              (report['PG.Q.Value'] <= 0.01) &
              (report['Global.Q.Value'] <= 0.01) &
              (report['Global.PG.Q.Value'] <= 0.01)]  # 0.01 = standard 1% FDR

# Pivot to a protein matrix from the filtered long report.
pg = filt.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
pg = np.log2(pg.replace(0, np.nan))  # DIA-NN writes 0 for not-quantified; log2(0) = -Inf
