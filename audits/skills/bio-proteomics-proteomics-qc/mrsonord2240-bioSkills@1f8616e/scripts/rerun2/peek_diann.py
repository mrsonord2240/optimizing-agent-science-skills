import pandas as pd
p='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/diann_libbased_mzml/diann_out/report.parquet'
d=pd.read_parquet(p)
print('shape',d.shape); print(list(d.columns))
print(d['Run'].value_counts().to_string())
