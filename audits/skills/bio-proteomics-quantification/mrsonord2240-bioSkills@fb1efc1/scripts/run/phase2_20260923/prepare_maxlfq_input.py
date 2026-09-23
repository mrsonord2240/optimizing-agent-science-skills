"""Prepare the documented long peptide-ion input from the audit MaxQuant evidence fixture."""
from pathlib import Path
import pandas as pd

run = Path(r"F:\OpenScience\audits\bio-proteomics-quantification\run\phase2_20260923")
data = Path(r"F:\OpenScience\audits\bio-proteomics-quantification\data")
ev = pd.read_csv(data / "evidence.txt", sep="\t", quotechar="\0", low_memory=False)
out = pd.DataFrame({"protein": ev["Proteins"], "ion": ev["Modified sequence"].astype(str) + "_" + ev["Charge"].astype(str), "run": ev["Raw file"], "intensity": pd.to_numeric(ev["Intensity"], errors="coerce")})
out = out[(out.intensity > 0) & out.protein.notna() & (out.protein != "")]
out.to_csv(run / "peptide_long.csv", index=False)
assert len(out) > 9000 and out.run.nunique() == 8
print(f"rows={len(out)} proteins={out.protein.nunique()} runs={out.run.nunique()}")
