"""
Re-auditor's independent reproduction script (fresh, not copied from the fixer's or
original auditor's scripts). Goal: verify, from first principles, whether the fixer's
claim that scvelo 0.3.4's mode='dynamical'/'stochastic' are genuinely broken against
numpy 2.5.3 / pandas 3.0.5 on this box, and whether either failure has a call-site fix
the fixer missed (e.g. a monkeypatch).

Part 0: isolate the claimed pandas.unique(list) regression WITHOUT scvelo at all.
Part 1: run scv.tl.recover_dynamics on real pancreas data fresh, capture traceback.
Part 2: monkeypatch pandas.unique (module-level) and re-try recover_dynamics to see if
        a call-site-only patch gets further, and if so, what breaks next.
Part 3: if align_dynamics is the next failure, try a call-site workaround (force adata
        copy / writable arrays before recover_dynamics) and see if that resolves it too.
Part 4: mode='stochastic' -> leastsq_generalized numpy incompatibility, fresh capture.
"""
import sys, traceback, copy as copy_mod

print("=" * 70)
print("PART 0: isolate pandas.unique(list) behavior directly, no scvelo")
print("=" * 70)
import pandas as pd
import numpy as np
print("pandas version:", pd.__version__, "numpy version:", np.__version__)
try:
    out = pd.unique(["A", "B", "A", "C"])
    print("pd.unique(list) SUCCEEDED:", out)
except Exception as e:
    print("pd.unique(list) FAILED:", type(e).__name__, "-", e)
try:
    out = pd.unique(np.array(["A", "B", "A", "C"]))
    print("pd.unique(ndarray) SUCCEEDED:", out)
except Exception as e:
    print("pd.unique(ndarray) FAILED:", type(e).__name__, "-", e)

print()
print("=" * 70)
print("PART 1: fresh recover_dynamics() on real pancreas data (no patch)")
print("=" * 70)
import scanpy as sc
import scvelo as scv
print("scvelo version:", scv.__version__)

DATA = r"F:\OpenScience\audits\bio-single-cell-trajectory-inference\data\pancreas_raw.h5ad"

def build_adata():
    adata = sc.read_h5ad(DATA)
    scv.pp.filter_and_normalize(adata, min_shared_counts=20)
    adata.layers["normalized_X"] = adata.X.copy()
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    adata = adata[:, adata.var["highly_variable"]].copy()
    adata.X = adata.layers.pop("normalized_X")
    scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
    return adata

adata1 = build_adata()
try:
    scv.tl.recover_dynamics(adata1, n_jobs=1)
    print("PART 1: recover_dynamics SUCCEEDED (unexpected)")
except Exception as e:
    print("PART 1: recover_dynamics FAILED:", type(e).__name__, "-", e)
    traceback.print_exc(limit=6)

print()
print("=" * 70)
print("PART 2: monkeypatch pandas.unique at module level, re-try recover_dynamics")
print("=" * 70)
# scvelo's make_unique_list does `from pandas import Index, unique` INSIDE the function
# body on every call, so patching the pandas module attribute before the call should be
# picked up even though scvelo never imported pandas.unique into its own namespace at
# import time.
_orig_unique = pd.unique
def _patched_unique(values, *a, **kw):
    if isinstance(values, (list, tuple)):
        values = np.asarray(values)
    return _orig_unique(values, *a, **kw)
pd.unique = _patched_unique
print("Patched pandas.unique to coerce list/tuple -> ndarray before calling through.")

adata2 = build_adata()
try:
    scv.tl.recover_dynamics(adata2, n_jobs=1)
    print("PART 2: recover_dynamics SUCCEEDED after monkeypatch (unexpected)")
except Exception as e:
    print("PART 2: recover_dynamics FAILED after monkeypatch:", type(e).__name__, "-", e)
    traceback.print_exc(limit=8)
finally:
    pd.unique = _orig_unique
    print("Restored original pandas.unique.")

print()
print("=" * 70)
print("PART 3: if PART 2 failed on a read-only array, try forcing writable layers")
print("=" * 70)
adata3 = build_adata()
pd.unique = _patched_unique
try:
    # Force every layer/X to be an owned, writable ndarray before recover_dynamics,
    # in case anndata handed back a read-only view (e.g. from a cached/backed store).
    import scipy.sparse as sp
    def force_writable(a):
        if sp.issparse(a.X):
            a.X = a.X.copy()
        else:
            a.X = np.array(a.X, copy=True)
            a.X.setflags(write=True)
        for k in list(a.layers.keys()):
            L = a.layers[k]
            if sp.issparse(L):
                a.layers[k] = L.copy()
            else:
                Lc = np.array(L, copy=True)
                Lc.setflags(write=True)
                a.layers[k] = Lc
        return a
    adata3 = force_writable(adata3)
    scv.tl.recover_dynamics(adata3, n_jobs=1)
    print("PART 3: recover_dynamics SUCCEEDED after monkeypatch + forced-writable layers")
except Exception as e:
    print("PART 3: recover_dynamics FAILED after monkeypatch + forced-writable layers:", type(e).__name__, "-", e)
    traceback.print_exc(limit=8)
finally:
    pd.unique = _orig_unique
    print("Restored original pandas.unique.")

print()
print("=" * 70)
print("PART 4: mode='stochastic' fresh capture (numpy>=2 scalar-coercion claim)")
print("=" * 70)
adata4 = build_adata()
try:
    scv.tl.velocity(adata4, mode="stochastic")
    print("PART 4: mode='stochastic' SUCCEEDED (unexpected)")
except Exception as e:
    print("PART 4: mode='stochastic' FAILED:", type(e).__name__, "-", e)
    traceback.print_exc(limit=8)

print()
print("DONE")
