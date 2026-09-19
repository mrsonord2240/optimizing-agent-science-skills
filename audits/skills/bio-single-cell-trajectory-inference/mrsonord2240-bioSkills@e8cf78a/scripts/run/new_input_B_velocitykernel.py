"""
Re-auditor NEW input B (not in the original 7, not verified by the fixer): CellRank 2's
VelocityKernel combined with a ConnectivityKernel, on real pancreatic endocrinogenesis
data, using the mode='deterministic' velocity the fix's compatibility note says is the
only mode that runs here. The original audit's Input 6 only exercised
PseudotimeKernel+ConnectivityKernel; VelocityKernel is a different, documented code
path (SKILL.md: "Velocity only when trustworthy") that neither the original audit nor
the fixer separately verified end-to-end with the fixed deterministic-mode velocity.
Tests whether the deterministic-mode velocity graph is actually USABLE downstream by
CellRank, not just internally self-consistent.
"""
import scanpy as sc
import numpy as np
import pandas as pd


def main():
    adata = sc.read_h5ad("data/pancreas_with_velocity.h5ad")

    import cellrank as cr
    vk = cr.kernels.VelocityKernel(adata).compute_transition_matrix(n_jobs=1)
    ck = cr.kernels.ConnectivityKernel(adata).compute_transition_matrix()
    combined = 0.8 * vk + 0.2 * ck

    g = cr.estimators.GPCCA(combined)
    g.compute_macrostates(n_states=8, cluster_key='clusters')
    g.predict_terminal_states(method='stability')
    g.predict_initial_states(n_states=1, allow_overlap=True)
    g.compute_fate_probabilities(n_jobs=1)

    print("macrostates:", list(g.macrostates.cat.categories))
    print("terminal_states:", list(g.terminal_states.cat.categories.dropna()) if g.terminal_states is not None else None)
    print("initial_states:", list(g.initial_states.cat.categories.dropna()) if g.initial_states is not None else None)

    fp = g.fate_probabilities
    fp_arr = fp.X if hasattr(fp, "X") else np.asarray(fp)
    fp_df = pd.DataFrame(fp_arr, index=adata.obs_names, columns=fp.names)
    ent = -(fp_df.clip(lower=1e-12) * np.log(fp_df.clip(lower=1e-12))).sum(axis=1)
    ductal_ent = ent[adata.obs["clusters"] == "Ductal"].mean()
    terminal_mask = adata.obs["clusters"].isin(["Alpha", "Beta"])
    terminal_ent = ent[terminal_mask].mean()
    print(f"Mean fate-probability entropy Ductal (progenitor): {ductal_ent:.4f}, Alpha/Beta (terminal): {terminal_ent:.4f}")
    print("ASSERTION ductal_entropy_higher_than_terminal:", bool(ductal_ent > terminal_ent))
    print("SUCCESS: VelocityKernel + deterministic-mode velocity ran end-to-end through CellRank")


if __name__ == "__main__":
    main()
