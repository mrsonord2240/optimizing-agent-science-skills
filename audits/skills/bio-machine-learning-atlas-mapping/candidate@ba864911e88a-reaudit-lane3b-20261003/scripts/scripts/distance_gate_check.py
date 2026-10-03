"""Independent check of the SKILL.md table column 'flagged by a reference-calibrated distance gate'.
runpy of the Skill's scarches_annotation.py (unmodified), then the ood_gating_demo-style gate on the real latent:
mean distance to 15 nearest reference cells, threshold = 99th pct of reference self-distances (leave-self-out)."""
import os, sys, shutil, runpy, json
import numpy as np
from sklearn.neighbors import NearestNeighbors
ST = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived"
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping"
case, tag = sys.argv[1], sys.argv[2]
ref = {"none": ST+r"\atlas-pair\reference_labeled.h5ad", "mono": ST+r"\atlas-pair-holdout\reference_no_monocytes.h5ad",
       "bcell": ST+r"\atlas-pair-holdout\reference_no_bcells.h5ad"}[case]
RUN = os.path.dirname(os.path.abspath(__file__))
w = os.path.join(RUN, "work", tag); shutil.rmtree(w, ignore_errors=True); os.makedirs(w); os.chdir(w)
shutil.copy(ref, "reference_labeled.h5ad"); shutil.copy(ST+r"\atlas-pair\query.h5ad", "query.h5ad")
g = runpy.run_path(SK + r"\scripts\scarches_annotation.py")
rl = g['ref_scanvi'].get_latent_representation(); ql = g['adata_query'].obsm['X_scANVI']
nn = NearestNeighbors(n_neighbors=16).fit(rl)
self_d = nn.kneighbors(rl)[0][:, 1:].mean(axis=1)
qd = nn.kneighbors(ql)[0][:, :15].mean(axis=1)
out = {}
for q in (99, 95):
    thr = np.percentile(self_d, q); flag = qd > thr
    out[f"p{q}"] = {"threshold": float(thr), "flagged_all": float(flag.mean())}
    drop = {"none": None, "mono": "Monocytes", "bcell": "B cells"}[case]
    if drop:
        m = (g['adata_query'].obs['truth_coarse'].astype(str) == drop).values
        out[f"p{q}"]["flagged_heldout_type"] = float(flag[m].mean()); out[f"p{q}"]["n_heldout"] = int(m.sum())
json.dump(out, open(os.path.join(RUN, f"distgate_{tag}.json"), "w"), indent=1); print(json.dumps(out, indent=1))
