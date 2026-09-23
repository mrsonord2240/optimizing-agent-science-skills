"""Phase 2 Input 1: execute the current SKILL.md Consensus Inference block on real PBMC data."""
from pathlib import Path

import liana as li
import scanpy as sc

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-communication")
OUT = ROOT / "run" / "phase2_20260923"
adata = sc.read_h5ad(ROOT / "data" / "adata_annotated.h5ad")

# Current SKILL.md block, changed only to use audited absolute paths and save evidence.
li.mt.rank_aggregate(adata, groupby="cell_type", resource_name="consensus",
                     expr_prop=0.1, use_raw=False, n_perms=1000, verbose=True)
res = adata.uns["liana_res"]
robust = res[(res["specificity_rank"] < 0.05) & (res["magnitude_rank"] < 0.05)]

assert {"magnitude_rank", "specificity_rank"}.issubset(res.columns)
assert len(res) > 1000 and len(robust) > 0
res.to_csv(OUT / "canonical_all_pairs.csv", index=False)
robust.to_csv(OUT / "canonical_robust_pairs.csv", index=False)
print("TOTAL_PAIRS", len(res))
print("ROBUST_PAIRS", len(robust))
print("TOP5")
print(robust.sort_values("magnitude_rank").head(5)[
    ["source", "target", "ligand_complex", "receptor_complex", "magnitude_rank", "specificity_rank"]
].to_string(index=False))
