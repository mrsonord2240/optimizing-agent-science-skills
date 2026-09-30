# Executes the SnapATAC2 code block extracted VERBATIM from the fixed references/ecosystem-workflows.md,
# with only path and slice-driven threshold substitutions (chr1 slice cannot meet min_counts=1000/min_tsse=4).
import os, re, time
SKILL=os.environ["SKILL"]; D=os.environ["ATACDATA"]; SCA=os.environ["SCA"]
md=open(f"{SKILL}/references/ecosystem-workflows.md",encoding="utf-8").read()
blk=[b for b in re.findall(r"```python\n(.*?)```",md,re.S) if "snapatac2" in b][0]
assert "sample_id" not in blk and "snap.pp.knn(data)" in blk and "n_jobs=1" in blk
code=(blk.replace("outs/fragments.tsv.gz",f"{D}/scatac/outs/fragments.tsv.gz")
         .replace("min_counts=1000, min_tsse=4","min_counts=400, min_tsse=0.3"))
wd=f"{SCA}/work/reaudit10x_snap"; os.makedirs(wd,exist_ok=True); os.chdir(wd)
if os.path.exists("out.h5ad"): os.remove("out.h5ad")
open("block_executed.py","w").write(code)
g={}; t=time.time(); exec(compile(code,"block","exec"),g)
data=g["data"]; o=data.obs[:]
print("n_obs",data.n_obs,"clusters",o["leiden"].value_counts().sort("count",descending=True).to_dicts())
print("obsp",list(data.obsp.keys()),"obsm",list(data.obsm.keys()),"uns",list(data.uns.keys()))
gm=g["gene_mat"]; print("gene_mat",gm.shape)
import numpy as np
tot=np.asarray(gm.X.sum(0)).ravel(); print("top genes",[gm.var_names[i] for i in np.argsort(-tot)[:8]])
print("seconds",round(time.time()-t))
data.close()
