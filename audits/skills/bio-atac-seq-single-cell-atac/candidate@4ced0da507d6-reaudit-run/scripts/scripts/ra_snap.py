# Re-audit: extract the SnapATAC2 block VERBATIM from the live references/ecosystem-workflows.md; only path and slice-driven filter substitutions.
import os, re, time
import numpy as np
SKILL=os.environ["SKILL"]; D=os.environ["ATACDATA"]; SCA=os.environ["SCA"]
md=open(f"{SKILL}/references/ecosystem-workflows.md",encoding="utf-8").read()
blk=[b for b in re.findall(r"```python\n(.*?)```",md,re.S) if "import_fragments" in b][0]
print("block mentions sample_id:", "sample_id" in blk, "| pp.knn:", "snap.pp.knn(data)" in blk, "| n_jobs=1:", "n_jobs=1" in blk)
assert "min_counts=1000, min_tsse=4" in blk
code=(blk.replace("outs/fragments.tsv.gz",f"{D}/scatac/outs/fragments.tsv.gz")
         .replace("min_counts=1000, min_tsse=4","min_counts=400, min_tsse=0.3"))
wd=f"{SCA}/work/ra_snap"; os.makedirs(wd,exist_ok=True); os.chdir(wd)
if os.path.exists("out.h5ad"): os.remove("out.h5ad")
import snapatac2 as snap
print("snapatac2",snap.__version__,"| has import_data:",hasattr(snap.pp,"import_data"),"| has import_fragments:",hasattr(snap.pp,"import_fragments"),"| has read_10x:",hasattr(snap,"read_10x"))
g={}; t=time.time(); exec(compile(code,"block","exec"),g)
data=g["data"]; o=data.obs[:]
print("n_obs",data.n_obs,"clusters",o["leiden"].value_counts().sort("count",descending=True).to_dicts())
print("obsp",list(data.obsp.keys()),"obsm",list(data.obsm.keys()),"uns keys",list(data.uns.keys()))
um=np.asarray(data.obsm["X_umap"]); print("umap",um.shape,"finite",bool(np.isfinite(um).all()))
ts=o["tsse"].to_numpy(); print("tsse range",round(float(ts.min()),2),round(float(ts.max()),2),"(filter >=0.3)")
sp=np.asarray(data.obsm["X_spectral"]); print("spectral",sp.shape)
gm=g["gene_mat"]; print("gene_mat",gm.shape)
tot=np.asarray(gm.X.sum(0)).ravel(); print("top genes",[gm.var_names[i] for i in np.argsort(-tot)[:8]])
print("seconds",round(time.time()-t))
data.close()
