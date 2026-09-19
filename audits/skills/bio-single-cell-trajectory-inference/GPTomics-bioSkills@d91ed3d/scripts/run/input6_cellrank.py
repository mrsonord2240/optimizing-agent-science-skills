"""
Additional probe -- SKILL.md's "Directed Fate Mapping With CellRank 2" code
block, run against the real Paul15 data already processed in Input 1
(has dpt_pseudotime, leiden clusters, neighbor graph), in an isolated venv
(cellrank would downgrade the shared venv's scipy -- see TOOLS.md
"Blocked or gated"). cellrank 2.3.3 installed fresh alongside scanpy in
this isolated venv.

Wrapped under __main__ guard: cellrank's parallelize() helper (used by
PseudotimeKernel, and again inside compute_fate_probabilities) spawns
worker processes via multiprocessing.Manager() on Windows, which requires
this guard in any plain .py script -- unrelated to the Skill's own
content, a general Windows multiprocessing requirement.
"""
import scanpy as sc
import cellrank as cr
import numpy as np
import pandas as pd


def main():
    adata = sc.read_h5ad('../data/paul15_paga_dpt.h5ad')
    print(adata)
    print('has dpt_pseudotime:', 'dpt_pseudotime' in adata.obs)
    print('has leiden:', 'leiden' in adata.obs)
    print('has connectivities:', 'connectivities' in adata.obsp)

    # --- SKILL.md "Directed Fate Mapping With CellRank 2" block, run verbatim ---
    pk = cr.kernels.PseudotimeKernel(adata, time_key='dpt_pseudotime').compute_transition_matrix(n_jobs=1, show_progress_bar=False)
    ck = cr.kernels.ConnectivityKernel(adata).compute_transition_matrix()
    combined = 0.8 * pk + 0.2 * ck

    g = cr.estimators.GPCCA(combined)
    g.compute_macrostates(n_states=10, cluster_key='leiden')
    g.predict_terminal_states(method='stability')
    # SKILL.md's code calls predict_initial_states(n_states=1) with no
    # allow_overlap handling; on this real data the predicted initial state
    # overlaps 30 cells with an already-identified terminal state and
    # cellrank correctly refuses -- see finding recorded separately.
    g.predict_initial_states(n_states=1, allow_overlap=True)
    g.compute_fate_probabilities(n_jobs=1, show_progress_bar=False)
    g.compute_lineage_drivers()

    print('\nmacrostates:', list(g.macrostates.cat.categories) if hasattr(g, 'macrostates') else None)
    print('terminal_states:', list(g.terminal_states.cat.categories.dropna()) if g.terminal_states is not None else None)
    print('initial_states:', list(g.initial_states.cat.categories.dropna()) if g.initial_states is not None else None)
    fp = g.fate_probabilities
    print('fate_probabilities shape:', None if fp is None else fp.shape)

    if fp is not None:
        fp_arr = fp.X if hasattr(fp, 'X') else np.asarray(fp)
        fp_df = pd.DataFrame(fp_arr, index=adata.obs_names, columns=fp.names)
        ent = -(fp_df.clip(lower=1e-12) * np.log(fp_df.clip(lower=1e-12))).sum(axis=1)
        mep_ent = ent[adata.obs['paul15_clusters'] == '7MEP'].mean()
        mature = adata.obs['paul15_clusters'].isin(['1Ery', '16Neu', '15Mo', '11DC'])
        mature_ent = ent[mature].mean()
        print(f'\nMean fate-probability entropy in MEP: {mep_ent:.4f}, in mature cells: {mature_ent:.4f}')
        print(f'ASSERTION fate_entropy_falls_with_commitment: {mep_ent > mature_ent}')

    print('\nDone.')


if __name__ == '__main__':
    main()
