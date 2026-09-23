"""Phase 2 Input 3: verify the current SKILL.md single-group boundary statement."""
from pathlib import Path

import liana as li
import scanpy as sc

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-communication")
adata = sc.read_h5ad(ROOT / "data" / "adata_annotated.h5ad")
adata.obs["single_group"] = "all_cells"
try:
    li.mt.rank_aggregate(adata, groupby="single_group", resource_name="consensus",
                         expr_prop=0.1, use_raw=False, n_perms=100, verbose=False)
except ValueError as exc:
    message = str(exc)
    assert "log2FC" in message and "no cells" in message.lower()
    print("EXPECTED_VALUE_ERROR")
    print(message)
else:
    raise AssertionError("Expected single-group LIANA call to raise ValueError")
