"""Independent parser assertions for fresh Phase-2 corrective persisted files."""
from pathlib import Path
import pandas as pd
r=Path(r"F:\OpenScience\audits\bio-proteomics-quantification\run\phase2_corrective_20260923")
m=pd.read_csv(r/"protein_abundance.csv")
i=pd.read_csv(r/"protein_maxlfq.csv",index_col=0)
d=pd.read_csv(r/"diann_maxlfq.csv",index_col=0)
assert m.shape[0]==2305 and m["Protein"].nunique()==296
assert i.shape==(299,8) and (r/"protein_maxlfq.csv.disconnected.txt").read_text().count("\n")>=3
assert d.shape==(947,8) and (r/"tmt10_corrected.rds").stat().st_size>1000
print(f"MSstats={m.shape[0]}x{m.shape[1]} proteins={m.Protein.nunique()} | MaxLFQ={i.shape} | DIA-NN-MaxLFQ={d.shape} | TMT-RDS=present")
