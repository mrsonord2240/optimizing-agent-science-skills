"""Delta rerun (2nd-fix interface): run the Skill's scarches_annotation.py (runpy, unmodified) from STAGED inputs, then
label_marker_check.py (a) with no flag (must exit 2 with a usage error, no verdict) and (b) with --markers curated JSON.
Also records which curated markers exist in the staged 1604-gene set. Reads only staged files; nothing to construct.
Usage: run_case.py <none|mono|bcell> <tag>   (e.g. run_case.py mono mono). Work dir: work/<tag>/ ; summary: summary_<tag>.json"""
import os, sys, shutil, runpy, json, subprocess, hashlib
import numpy as np, scanpy as sc
ST = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived"
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping"
MK = os.path.join(SK, "references", "pbmc-markers.json")
CHK = os.path.join(SK, "scripts", "label_marker_check.py")
RUN = os.path.dirname(os.path.abspath(__file__))
case, tag = sys.argv[1], sys.argv[2]
ref = {"none": ST+r"\atlas-pair\reference_labeled.h5ad", "mono": ST+r"\atlas-pair-holdout\reference_no_monocytes.h5ad",
       "bcell": ST+r"\atlas-pair-holdout\reference_no_bcells.h5ad"}[case]
w = os.path.join(RUN, "work", tag); shutil.rmtree(w, ignore_errors=True); os.makedirs(w); os.chdir(w)
shutil.copy(ref, "reference_labeled.h5ad"); shutil.copy(ST+r"\atlas-pair\query.h5ad", "query.h5ad")
g = runpy.run_path(os.path.join(SK, "scripts", "scarches_annotation.py"))
q = g['adata_query']; pred = q.obs['predicted_label'].astype(str); truth = q.obs['truth_coarse'].astype(str)
drop = {"none": None, "mono": "Monocytes", "bcell": "B cells"}[case]
m = (truth == drop) if drop else np.ones(len(q), bool)
out = {"case": case, "n_target": int(m.sum()), "pct_unknown_knn_gate": float((pred[m] == 'Unknown').mean()),
       "top_pred": pred[m].value_counts().head(4).to_dict(),
       "query_annotated_sha256": hashlib.sha256(open("query_annotated.h5ad","rb").read()).hexdigest()}
mk = json.load(open(MK))
out["markers_present_in_1604"] = {l: {"present": [x for x in gs if x in q.var_names], "absent": [x for x in gs if x not in q.var_names]} for l, gs in mk.items()}
py = sys.executable
r = subprocess.run([py, CHK], capture_output=True, text=True)
out["marker_noflag_rc"] = r.returncode; out["marker_noflag_stderr"] = r.stderr.strip().splitlines()[-2:]; out["marker_noflag_stdout"] = r.stdout.strip()
r = subprocess.run([py, CHK, "--markers", MK, "--out", "marker_curated.tsv"], capture_output=True, text=True)
out["marker_curated_rc"] = r.returncode; out["marker_curated"] = r.stdout.strip().splitlines()
json.dump(out, open(os.path.join(RUN, f"summary_{tag}.json"), "w"), indent=1); print(json.dumps(out, indent=1))
