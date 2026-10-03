"""Held-out cell-type OOD check: drop one label from the reference, run the Skill's scarches_annotation.py UNMODIFIED
(runpy), then report how query cells of the dropped type were handled.
Usage: heldout_ood.py <label-to-drop|NONE>   (cwd = a fresh work dir)"""
import os, sys, shutil, runpy, json
import numpy as np, pandas as pd, scanpy as sc
from sklearn.neighbors import NearestNeighbors
PAIR = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\atlas-pair"
SKILL = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping\scripts\scarches_annotation.py"
drop = sys.argv[1]
w = os.path.join(os.getcwd(), "run_" + drop.replace(" ", "_").replace("/", "_")); shutil.rmtree(w, ignore_errors=True); os.makedirs(w); os.chdir(w)
ref = sc.read_h5ad(os.path.join(PAIR, "reference_labeled.h5ad"))
if drop != "NONE":
    ref = ref[ref.obs['cell_type'] != drop].copy()
ref.write_h5ad("reference_labeled.h5ad"); shutil.copy(os.path.join(PAIR, "query.h5ad"), "query.h5ad")
print("reference label counts:", ref.obs['cell_type'].value_counts().to_dict())
g = runpy.run_path(SKILL)
q, qm, unc, aref = g['adata_query'], g['query_scanvi'], g['uncertainty'], g['adata_ref']
truth = q.obs['truth_coarse'].astype(str); pred = q.obs['predicted_label'].astype(str)
proba = qm.predict(soft=True)
print("predict(soft=True) type:", type(proba).__name__, proba.shape)
softmax_max = np.asarray(proba).max(axis=1)
# alternative distance gate on the scANVI latent (calibrated on the reference itself, 99th pct of 15-NN mean distance)
rl = g['ref_scanvi'].get_latent_representation(); ql = q.obsm['X_scANVI']
nn = NearestNeighbors(n_neighbors=16).fit(rl)
ref_self = nn.kneighbors(rl)[0][:, 1:].mean(axis=1); thr = np.percentile(ref_self, 99)
qd = nn.kneighbors(ql, n_neighbors=15)[0].mean(axis=1)
out = {"dropped": drop, "query_n": int(len(q)), "dist_threshold": float(thr)}
mask = (truth == drop) if drop != "NONE" else np.zeros(len(q), bool)
def rep(m, name):
    if m.sum() == 0: return
    out[name] = {"n": int(m.sum()), "pct_unknown_knn_gate": float((pred[m] == 'Unknown').mean()),
                 "pct_softmax_ge_0.5": float((softmax_max[m] >= 0.5).mean()), "mean_softmax_max": float(softmax_max[m].mean()),
                 "mean_knn_uncertainty": float(unc[m].mean()), "pct_dist_gate_flagged": float((qd[m] > thr).mean()),
                 "pct_predicted_confident_wrong_label(not Unknown)": float((pred[m] != 'Unknown').mean()),
                 "top_predicted": pred[m].value_counts().head(4).to_dict()}
rep(mask, "heldout_type_cells"); rep(~mask, "other_cells")
out["overall_unknown_pct"] = float((pred == 'Unknown').mean())
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(w), "heldout_" + drop.replace(" ", "_").replace("/", "_") + ".json"), "w"), indent=1)
