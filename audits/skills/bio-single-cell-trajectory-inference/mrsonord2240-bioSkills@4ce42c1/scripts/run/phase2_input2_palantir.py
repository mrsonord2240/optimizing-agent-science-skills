"""Phase 2 Input 2: Palantir fate probabilities on real branching progenitors."""
import numpy as np
import palantir
import scanpy as sc

adata = sc.read_h5ad(r"F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-trajectory-inference\data\paul15_paga_dpt.h5ad")
root_idx = np.flatnonzero(adata.obs["paul15_clusters"] == "7MEP")
assert len(root_idx), "No MEP root available"
dm = palantir.utils.run_diffusion_maps(adata, n_components=5)
multi = palantir.utils.determine_multiscale_space(dm)
result = palantir.core.run_palantir(multi, early_cell=adata.obs_names[root_idx[0]], terminal_states=None, num_waypoints=500)
mep_entropy = float(result.entropy[adata.obs["paul15_clusters"] == "7MEP"].mean())
mature_mask = adata.obs["paul15_clusters"].isin(["1Ery", "16Neu", "15Mo"]).to_numpy()
mature_entropy = float(result.entropy[mature_mask].mean())
terminal_count = len(result.branch_probs.columns)
print(f"terminal_states={terminal_count}; MEP_entropy={mep_entropy:.4f}; mature_entropy={mature_entropy:.4f}")
print(f"ASSERTION_entropy_falls_with_commitment={mep_entropy > mature_entropy}")
