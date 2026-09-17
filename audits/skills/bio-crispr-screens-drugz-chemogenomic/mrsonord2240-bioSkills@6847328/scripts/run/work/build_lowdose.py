"""Build a 3-dose count table (Veh, LowDose, MidDose, HighDose=Drug) for the multi-dose
consistency check (Input 3). LowDose is the geometric mean of Veh and MidDose reads per
guide, matching the fix log's own approach ("low = geometric mean of vehicle and mid").
All three source files share identical guide order (verified: diff -q on column 1), so a
straight column-wise merge is safe.
"""
import pandas as pd
import numpy as np

DATA = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\data"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work"

std = pd.read_csv(f"{DATA}\\synthetic_drug_vehicle_counts.txt", sep="\t")
mid = pd.read_csv(f"{DATA}\\synthetic_middose_counts.txt", sep="\t")

assert (std["GUIDE"] == mid["GUIDE"]).all()

out = std[["GUIDE", "GENE", "T0", "Veh_r1", "Veh_r2", "Veh_r3"]].copy()
for r in (1, 2, 3):
    veh = std[f"Veh_r{r}"].astype(float)
    middose = mid[f"MidDose_r{r}"].astype(float)
    out[f"LowDose_r{r}"] = np.sqrt(np.maximum(veh, 1) * np.maximum(middose, 1)).round().astype(int)

for r in (1, 2, 3):
    out[f"MidDose_r{r}"] = mid[f"MidDose_r{r}"]
for r in (1, 2, 3):
    out[f"Drug_r{r}"] = std[f"Drug_r{r}"]

out.to_csv(f"{OUT}\\threedose_counts.txt", sep="\t", index=False)
print("wrote", f"{OUT}\\threedose_counts.txt", "rows:", len(out))
print(out.head(2).to_string())
