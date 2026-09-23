"""Phase 2 Input 5: execute the current SKILL.md resource-sensitivity block."""
from pathlib import Path

from liana.method import cellphonedb
import scanpy as sc

AUDIT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-communication")
OUT = AUDIT / "run" / "phase2_20260923"
adata = sc.read_h5ad(AUDIT / "data" / "adata_annotated.h5ad")
resources = ["consensus", "cellphonedb", "cellchatdb"]
for resource in resources:
    cellphonedb(adata, groupby="cell_type", resource_name=resource,
                expr_prop=0.1, use_raw=False, key_added=f"cpdb_{resource}", verbose=False)

top_sets = {}
for resource in resources:
    frame = adata.uns[f"cpdb_{resource}"]
    assert "cellphone_pvals" in frame and len(frame) > 100
    sig = frame[frame["cellphone_pvals"] < 0.05]
    top_sets[resource] = set(zip(sig["source"], sig["target"], sig["ligand_complex"], sig["receptor_complex"]))
    frame.to_csv(OUT / f"resource_{resource}.csv", index=False)
    print(resource, "PAIRS", len(frame), "SIGNIFICANT", len(top_sets[resource]))
survive = set.intersection(*top_sets.values())
assert len(survive) > 0
print("SURVIVE_ALL_THREE", len(survive))
print("SAMPLE", sorted(survive)[:5])
