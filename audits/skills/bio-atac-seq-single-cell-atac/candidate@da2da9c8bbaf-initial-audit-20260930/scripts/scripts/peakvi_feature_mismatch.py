# Does PEAKVI.load_query_data (the Skill's scArches call) silently accept a query whose peak set differs from the reference's? (real PBMC 5k chr1 slice; reference from peakvi_query.py)
import os, warnings, numpy as np, scanpy as sc, scvi, scipy.sparse as sp
SCA=os.environ["SCA"]; D=os.environ["ATACDATA"]; os.chdir(f"{SCA}/work"); scvi.settings.seed=0
ad=sc.read_10x_h5(f"{D}/scatac/outs/filtered_peak_bc_matrix.h5", gex_only=False); ad.X=(ad.X>0).astype(np.float32)
sc.pp.filter_cells(ad,min_genes=200); sc.pp.filter_genes(ad,min_cells=20)
rng=np.random.default_rng(0); q=ad[rng.permutation(ad.n_obs)[:ad.n_obs//4]].copy()
ref_path=f"{SCA}/work/peakvi_ref"
ref_vars=set(scvi.model.PEAKVI.load(ref_path, adata=None).adata.var_names) if False else None
# 1) query with only a random 60% of the reference peaks (shuffled order), 2) query with renamed (non-matching) peaks
keep=rng.permutation(q.n_vars)[:int(.6*q.n_vars)]; q1=q[:,keep].copy()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    try:
        m=scvi.model.PEAKVI.load_query_data(q1, ref_path); print("60% peaks: ACCEPTED, query n_vars after load", m.adata.n_vars, " warnings:", [str(x.message)[:120] for x in w][:3])
    except Exception as e: print("60% peaks: RAISED", type(e).__name__, str(e)[:200])
q2=q.copy(); q2.var_names=[f"chrZ:{i}-{i+500}" for i in range(q2.n_vars)]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    try:
        m=scvi.model.PEAKVI.load_query_data(q2, ref_path); print("no shared peaks: ACCEPTED, n_vars", m.adata.n_vars, " warnings:", [str(x.message)[:120] for x in w][:3])
        z=m.get_latent_representation(); print("latent finite", bool(np.isfinite(z).all()), z.shape)
    except Exception as e: print("no shared peaks: RAISED", type(e).__name__, str(e)[:200])
