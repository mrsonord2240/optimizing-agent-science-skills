"""
Re-auditor regression, input 6 (CellRank 2 directed fate mapping), fresh script
transcribed from the FIXED worktree SKILL.md's "Directed Fate Mapping With CellRank 2"
block verbatim, run against real Paul15 branching data already carrying dpt_pseudotime
and leiden clusters. Confirms the RuntimeError the original audit hit is gone with the
allow_overlap=True fix and the __main__ guard, and that the result is biologically sane.
"""
import scanpy as sc
import numpy as np
import pandas as pd


def main():
    adata = sc.read_h5ad("data/paul15_paga_dpt.h5ad")
    print(adata)

    # --- verbatim from fixed SKILL.md "Directed Fate Mapping With CellRank 2" ---
    import cellrank as cr
    pk = cr.kernels.PseudotimeKernel(adata, time_key='dpt_pseudotime').compute_transition_matrix(n_jobs=1)
    ck = cr.kernels.ConnectivityKernel(adata).compute_transition_matrix()
    combined = 0.8 * pk + 0.2 * ck

    g = cr.estimators.GPCCA(combined)
    g.compute_macrostates(n_states=10, cluster_key='leiden')
    g.predict_terminal_states(method='stability')
    g.predict_initial_states(n_states=1, allow_overlap=True)
    g.compute_fate_probabilities(n_jobs=1)
    g.compute_lineage_drivers()
    # --- end verbatim block ---

    print("macrostates:", list(g.macrostates.cat.categories))
    print("terminal_states:", list(g.terminal_states.cat.categories.dropna()) if g.terminal_states is not None else None)
    print("initial_states:", list(g.initial_states.cat.categories.dropna()) if g.initial_states is not None else None)

    fp = g.fate_probabilities
    fp_arr = fp.X if hasattr(fp, "X") else np.asarray(fp)
    fp_df = pd.DataFrame(fp_arr, index=adata.obs_names, columns=fp.names)
    ent = -(fp_df.clip(lower=1e-12) * np.log(fp_df.clip(lower=1e-12))).sum(axis=1)
    mep_ent = ent[adata.obs["paul15_clusters"] == "7MEP"].mean()
    mature = adata.obs["paul15_clusters"].isin(["1Ery", "16Neu", "15Mo", "11DC"])
    mature_ent = ent[mature].mean()
    print(f"Mean fate-probability entropy MEP: {mep_ent:.4f}, mature: {mature_ent:.4f}")
    print("ASSERTION fate_entropy_falls_with_commitment:", bool(mep_ent > mature_ent))
    print("SUCCESS: no RuntimeError, no ValueError")


if __name__ == "__main__":
    main()
