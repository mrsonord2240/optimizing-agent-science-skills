# specialized-topics.md scArches/PEAKVI block: reference train+save, then PEAKVI.load_query_data + train + latent, on real PBMC 5k chr1-slice peak matrix
import os, numpy as np, scanpy as sc, scvi, torch, scipy.sparse as sp
SCA=os.environ["SCA"]; D=os.environ["ATACDATA"]; os.chdir(f"{SCA}/work"); scvi.settings.seed=0
print("scvi",scvi.__version__,"torch",torch.__version__,"cuda",torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")
ad = sc.read_10x_h5(f"{D}/scatac/outs/filtered_peak_bc_matrix.h5", gex_only=False)
print(ad)
ad.X = (ad.X>0).astype(np.float32) if sp.issparse(ad.X) else ad.X
sc.pp.filter_cells(ad, min_genes=200); sc.pp.filter_genes(ad, min_cells=20)
print("after filter", ad.shape)
rng=np.random.default_rng(0); idx=rng.permutation(ad.n_obs); q=idx[:ad.n_obs//4]; r=idx[ad.n_obs//4:]
ref=ad[r].copy(); qry=ad[q].copy()
scvi.model.PEAKVI.setup_anndata(ref)
m=scvi.model.PEAKVI(ref); m.train(max_epochs=30, accelerator="auto")
ref_path=f"{SCA}/work/peakvi_ref"; m.save(ref_path, overwrite=True)
zr=m.get_latent_representation(); print("ref latent", zr.shape, "finite", bool(np.isfinite(zr).all()))
# as documented:
query_model = scvi.model.PEAKVI.load_query_data(qry, ref_path)
query_model.train(max_epochs=200, plan_kwargs=dict(weight_decay=0.0)) if False else query_model.train(max_epochs=30)
qry.obsm['X_emb'] = query_model.get_latent_representation()
print("query latent", qry.obsm['X_emb'].shape, "finite", bool(np.isfinite(qry.obsm['X_emb']).all()))
# sanity: query cells embedded in reference space -> nearest reference neighbours by depth-independent structure
from sklearn.neighbors import NearestNeighbors
nn=NearestNeighbors(n_neighbors=15).fit(zr); d,i=nn.kneighbors(qry.obsm['X_emb'])
rd=np.asarray(ref.X.sum(1)).ravel(); qd=np.asarray(qry.X.sum(1)).ravel()
print("median dist q->ref", round(float(np.median(d)),3), " median ref-ref", round(float(np.median(NearestNeighbors(n_neighbors=16).fit(zr).kneighbors(zr)[0][:,1:])),3))
print("doc call `train(max_epochs=200)` ok pattern executed with 30 epochs (bounded)")
