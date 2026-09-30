# specialized-topics.md PEAKVI block (peak-set alignment lines) on the real PBMC 5k chr1-slice peak matrix; query columns deliberately shuffled
import os, warnings, numpy as np, scanpy as sc, scvi, scipy.sparse as sp
SCA=os.environ["SCA"]; D=os.environ["ATACDATA"]; os.chdir(f"{SCA}/work"); scvi.settings.seed=0
ad=sc.read_10x_h5(f"{D}/scatac/outs/filtered_peak_bc_matrix.h5",gex_only=False); ad.X=(ad.X>0).astype(np.float32)
sc.pp.filter_cells(ad,min_genes=200); sc.pp.filter_genes(ad,min_cells=20)
rng=np.random.default_rng(0); idx=rng.permutation(ad.n_obs); q=idx[:ad.n_obs//4]; r=idx[ad.n_obs//4:]
adata_ref=ad[r].copy(); adata_query=ad[q].copy()
scvi.model.PEAKVI.setup_anndata(adata_ref); m=scvi.model.PEAKVI(adata_ref); m.train(max_epochs=30,accelerator="auto")
reference_path=f"{SCA}/work/reaudit10x_peakvi_ref"; m.save(reference_path,overwrite=True); zr=m.get_latent_representation()
perm=rng.permutation(adata_query.n_vars); shuffled=adata_query[:,perm].copy()   # simulates a query quantified in a different peak order
from sklearn.neighbors import NearestNeighbors
def qdist(model,a):
    z=model.get_latent_representation(); return float(np.median(NearestNeighbors(n_neighbors=15).fit(zr).kneighbors(z)[0]))
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    m_bad=scvi.model.PEAKVI.load_query_data(shuffled.copy(),reference_path); m_bad.train(max_epochs=30)
    print("WITHOUT alignment: warnings:",[str(x.message)[:90] for x in w if "var_names" in str(x.message)][:1],"median q->ref dist",round(qdist(m_bad,shuffled),3))
# --- documented lines ---
adata_query = shuffled[:, adata_ref.var_names].copy()
assert list(adata_query.var_names) == list(adata_ref.var_names)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    query_model = scvi.model.PEAKVI.load_query_data(adata_query, reference_path)
    print("WITH alignment: var_names warnings:",len([x for x in w if "var_names" in str(x.message)]))
query_model.train(max_epochs=30)
adata_query.obsm['X_emb'] = query_model.get_latent_representation()
print("aligned: latent",adata_query.obsm['X_emb'].shape,"finite",bool(np.isfinite(adata_query.obsm['X_emb']).all()),"median q->ref dist",round(qdist(query_model,adata_query),3),"ref-ref",round(float(np.median(NearestNeighbors(n_neighbors=16).fit(zr).kneighbors(zr)[0][:,1:])),3))
