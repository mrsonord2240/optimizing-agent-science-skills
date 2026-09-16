import numpy as np
import pandas as pd

report = pd.read_parquet('report.parquet')  # report.tsv dropped as default in DIA-NN 2.0
report = report[(report['Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.01)
                & (report['Global.PG.Q.Value'] <= 0.01)]  # run-level AND experiment-wide 1% FDR before quant

matrix = report.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
matrix = np.log2(matrix.replace(0, np.nan))  # PG.MaxLFQ can be 0 too; log2(0) = -inf
