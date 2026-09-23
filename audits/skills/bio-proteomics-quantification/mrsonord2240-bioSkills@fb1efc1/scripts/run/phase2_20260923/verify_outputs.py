"""Assert persisted Phase-2 outputs, independent of each producing process's exit status."""
from pathlib import Path
import pandas as pd

run = Path(r"F:\OpenScience\audits\bio-proteomics-quantification\run\phase2_20260923")
ms = pd.read_csv(run / "protein_abundance.csv")
iq = pd.read_csv(run / "protein_maxlfq.csv", index_col=0)
diann = pd.read_csv(run / "diann_maxlfq.csv", index_col=0)
assert ms.shape[0] == 2305 and ms["Protein"].nunique() == 296
assert iq.shape == (299, 8) and (run / "protein_maxlfq.csv.disconnected.txt").read_text().count("\n") >= 3
assert diann.shape == (947, 8)
assert (run / "tmt10_corrected.rds").stat().st_size > 1000
print(f"MSstats={ms.shape[0]}x{ms.shape[1]} proteins={ms.Protein.nunique()} | MaxLFQ={iq.shape} | DIA-NN-MaxLFQ={diann.shape} | TMT-RDS=present")
