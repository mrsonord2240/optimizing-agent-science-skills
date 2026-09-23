"""Phase 2 Input 6: CellRank 2 fate mapping through the shipped script interface."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc

SOURCE_SCRIPT = Path(r"F:\OpenScience\wt\single-cell-trajectory-inference\single-cell\trajectory-inference\scripts\cellrank_fate.py")


def main():
    assert "if __name__ == '__main__':" in SOURCE_SCRIPT.read_text(encoding="utf-8"), "Shipped Windows guard is missing"
    adata = sc.read_h5ad(r"F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-trajectory-inference\data\paul15_paga_dpt.h5ad")
    sys.path.insert(0, str(SOURCE_SCRIPT.parent))
    from cellrank_fate import fate_entropy, run_fate_mapping  # audited shipped functions
    g = run_fate_mapping(adata, time_key="dpt_pseudotime", cluster_key="leiden", n_states=10, w_pseudotime=0.8)
    entropy = fate_entropy(g, adata)
    mep = float(entropy[adata.obs["paul15_clusters"] == "7MEP"].mean())
    mature = float(entropy[adata.obs["paul15_clusters"].isin(["1Ery", "16Neu", "15Mo", "11DC"])].mean())
    print("macrostates=", list(g.macrostates.cat.categories))
    print(f"MEP_entropy={mep:.4f}; mature_entropy={mature:.4f}")
    print(f"ASSERTION_fate_entropy_falls_with_commitment={mep > mature}")


if __name__ == "__main__":
    main()
