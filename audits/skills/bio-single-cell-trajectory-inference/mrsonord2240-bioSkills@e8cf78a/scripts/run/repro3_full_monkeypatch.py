"""
Re-auditor probe: is there a call-site-only monkeypatch (no edits to scvelo's shipped
files) that gets mode='dynamical' fully working on this stack (scvelo 0.3.4, numpy
2.5.3, pandas 3.0.5)? Root cause of the 2nd bug, confirmed independently in
repro2_align_dynamics.py: scvelo.tools._em_model_core._read_pars() does
`adata.var[pkey].values`, which under pandas 3.x's always-on Copy-on-Write returns a
READ-ONLY ndarray; align_dynamics() then tries in-place `alpha[idx] = alpha[idx] / m_`
on that read-only array.

This monkeypatches BOTH pandas.unique (bug 1) AND
scvelo.tools._em_model_core._read_pars (bug 2) purely from the calling script, with no
edits under site-packages, and checks whether recover_dynamics() then completes.
"""
import multiprocessing as mp


def main():
    import numpy as np
    import pandas as pd
    import scanpy as sc
    import scvelo as scv
    import scvelo.tools._em_model_core as em_core

    print("scvelo:", scv.__version__, "numpy:", np.__version__, "pandas:", pd.__version__)

    DATA = r"F:\OpenScience\audits\bio-single-cell-trajectory-inference\data\pancreas_raw.h5ad"

    def build_small_adata(n_genes=40):
        adata = sc.read_h5ad(DATA)
        scv.pp.filter_and_normalize(adata, min_shared_counts=20)
        adata.layers["normalized_X"] = adata.X.copy()
        sc.pp.log1p(adata)
        sc.pp.highly_variable_genes(adata, n_top_genes=2000)
        adata = adata[:, adata.var["highly_variable"]].copy()
        adata.X = adata.layers.pop("normalized_X")
        scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
        adata = adata[:, :n_genes].copy()
        return adata

    # --- monkeypatch 1: pandas.unique must accept plain lists (bug 1, make_unique_list) ---
    _orig_unique = pd.unique

    def _patched_unique(values, *a, **kw):
        if isinstance(values, (list, tuple)):
            values = np.asarray(values)
        return _orig_unique(values, *a, **kw)

    # --- monkeypatch 2: _read_pars must return WRITABLE arrays (bug 2, align_dynamics) ---
    _orig_read_pars = em_core._read_pars

    def _patched_read_pars(adata, pars_names=None, key="fit"):
        pars = _orig_read_pars(adata, pars_names=pars_names, key=key)
        return [np.array(p, copy=True) for p in pars]

    adata = build_small_adata()
    pd.unique = _patched_unique
    em_core._read_pars = _patched_read_pars
    try:
        scv.tl.recover_dynamics(adata, n_jobs=1, var_names="all")
        print("recover_dynamics SUCCEEDED with the dual monkeypatch (call-site only, no scvelo file edits)")
        has_latent = "fit_alpha" in adata.var.columns
        print("fit_alpha present:", has_latent)
        scv.tl.latent_time(adata)
        print("latent_time computed OK:", "latent_time" in adata.obs.columns)
        print(adata.obs["latent_time"].describe())
    except Exception as e:
        print("recover_dynamics STILL FAILED with the dual monkeypatch:", type(e).__name__, "-", e)
        import traceback
        traceback.print_exc(limit=10)
    finally:
        pd.unique = _orig_unique
        em_core._read_pars = _orig_read_pars

    print("DONE")


if __name__ == "__main__":
    mp.freeze_support()
    main()
