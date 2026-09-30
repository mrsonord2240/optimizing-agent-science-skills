# Re-audit: PEAKVI block from live specialized-topics.md (alignment lines verbatim) on the real PBMC 5k chr1 peak matrix; query columns shuffled.
import os, re, warnings, numpy as np, scanpy as sc, scvi
SKILL=os.environ["SKILL"]; SCA=os.environ["SCA"]; D=os.environ["ATACDATA"]; os.chdir(f"{SCA}/work"); scvi.settings.seed=0
md=open(f"{SKILL}/references/specialized-topics.md",encoding="utf-8").read()
blk=[b for b in re.findall(r"```python\n(.*?)```",md,re.S) if "PEAKVI.load_query_data" in b][0]
print("doc has alignment lines:", "adata_query[:, adata_ref.var_names]" in blk and "assert list(adata_query.var_names)" in blk)
ad=sc.read_10x_h5(f"{D}/scatac/outs/filtered_peak_bc_matrix.h5",gex_only=False); ad.X=(ad.X>0).astype(np.float32)
sc.pp.filter_cells(ad,min_genes=200); sc.pp.filter_genes(ad,min_cells=20)
rng=np.random.default_rng(1); idx=rng.permutation(ad.n_obs); q=idx[:ad.n_obs//4]; r=idx[ad.n_obs//4:]
adata_ref=ad[r].copy(); adata_query=ad[q].copy()
scvi.model.PEAKVI.setup_anndata(adata_ref); m=scvi.model.PEAKVI(adata_ref); m.train(max_epochs=30,accelerator="auto")
reference_path=f"{SCA}/work/ra_peakvi_ref"; m.save(reference_path,overwrite=True); zr=m.get_latent_representation()
from sklearn.neighbors import NearestNeighbors
nn=NearestNeighbors(n_neighbors=15).fit(zr)
perm=rng.permutation(adata_query.n_vars); shuffled=adata_query[:,perm].copy()
# execute the documented block with the query shuffled and epochs bounded (200 -> 30); reference_path and adata_ref provided
code=blk.replace("max_epochs=200","max_epochs=30")
code="\n".join(l for l in code.splitlines() if not l.strip().startswith("adata_query") or "var_names" in l or "obsm" in l)
g={"adata_query":shuffled.copy(),"adata_ref":adata_ref,"reference_path":reference_path,"scvi":scvi}
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always"); exec(compile(code,"block","exec"),g)
print("var_names warnings with documented alignment:",len([x for x in w if "var_names" in str(x.message)]))
aq=g["adata_query"]; z=g["query_model"].get_latent_representation()
print("aligned latent",z.shape,"finite",bool(np.isfinite(z).all()),"X_emb",aq.obsm["X_emb"].shape)
print("median q->ref NN",round(float(np.median(nn.kneighbors(z)[0])),3),"ref-ref",round(float(np.median(NearestNeighbors(n_neighbors=16).fit(zr).kneighbors(zr)[0][:,1:])),3))
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    mb=scvi.model.PEAKVI.load_query_data(shuffled.copy(),reference_path); mb.train(max_epochs=30)
print("UNALIGNED: warnings",[str(x.message)[:80] for x in w if "var_names" in str(x.message)][:1],"median q->ref NN",round(float(np.median(nn.kneighbors(mb.get_latent_representation())[0])),3))
