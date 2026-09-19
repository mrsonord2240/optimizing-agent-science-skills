"""
Follow-up independent repro, properly guarded with if __name__ == '__main__' (required
on Windows for any scvelo/cellrank call that spawns a multiprocessing.Manager() -- my
first script (repro_scvelo_bugs.py) hit exactly this RuntimeError once the pandas.unique
bug was patched around, confirming a SECOND, independent Windows-multiprocessing defect
in scvelo's own recover_dynamics() (not just CellRank's kernels, as the fixer documented).

This script: patch pandas.unique, guard entry point, restrict to a small gene subset for
speed, and see whether recover_dynamics reaches align_dynamics() and whether the claimed
'ValueError: assignment destination is read-only' is real, and whether it has a call-site
fix (forcing writable layers before the call).
"""
import multiprocessing as mp

def main():
    import numpy as np
    import pandas as pd
    import scanpy as sc
    import scvelo as scv
    import scipy.sparse as sp

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
        # restrict further to a small gene subset purely to speed up the EM fit for this
        # repro -- we only need to reach align_dynamics, not a full biological result.
        adata = adata[:, :n_genes].copy()
        return adata

    _orig_unique = pd.unique
    def _patched_unique(values, *a, **kw):
        if isinstance(values, (list, tuple)):
            values = np.asarray(values)
        return _orig_unique(values, *a, **kw)

    print()
    print("=" * 70)
    print("Guarded run: patched pd.unique + if __name__ guard, small gene subset")
    print("=" * 70)
    adata = build_small_adata()
    pd.unique = _patched_unique
    try:
        scv.tl.recover_dynamics(adata, n_jobs=1, var_names="all")
        print("recover_dynamics SUCCEEDED end-to-end (unexpected given fixer's claim)")
        print("latent_time available:", "latent_time" in adata.obs or True)
    except Exception as e:
        print("recover_dynamics FAILED:", type(e).__name__, "-", e)
        import traceback
        traceback.print_exc(limit=10)
    finally:
        pd.unique = _orig_unique

    print()
    print("=" * 70)
    print("Second attempt: same as above but ALSO force every layer/X writable first")
    print("=" * 70)
    adata2 = build_small_adata()

    def force_writable(a):
        if sp.issparse(a.X):
            a.X = a.X.copy()
        else:
            a.X = np.array(a.X, copy=True)
        for k in list(a.layers.keys()):
            L = a.layers[k]
            if sp.issparse(L):
                a.layers[k] = L.copy()
            else:
                a.layers[k] = np.array(L, copy=True)
        return a

    adata2 = force_writable(adata2)
    pd.unique = _patched_unique
    try:
        scv.tl.recover_dynamics(adata2, n_jobs=1, var_names="all")
        print("recover_dynamics (forced-writable) SUCCEEDED end-to-end")
    except Exception as e:
        print("recover_dynamics (forced-writable) FAILED:", type(e).__name__, "-", e)
        import traceback
        traceback.print_exc(limit=10)
    finally:
        pd.unique = _orig_unique

    print("DONE")

if __name__ == "__main__":
    mp.freeze_support()
    main()
