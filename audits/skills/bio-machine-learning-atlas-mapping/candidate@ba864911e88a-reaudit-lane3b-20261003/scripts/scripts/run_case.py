"""Delta rerun: run the Skill's scarches_annotation.py (runpy, unmodified) from STAGED inputs, then both marker checks.
Usage: run_case.py <none|mono|bcell> <tag>. Work dir: work/<tag>/ ; summary: summary_<tag>.json"""
import os, sys, shutil, runpy, json, subprocess, hashlib
import numpy as np, scanpy as sc
ST = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived"
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping"
RUN = os.path.dirname(os.path.abspath(__file__))
case, tag = sys.argv[1], sys.argv[2]
ref = {"none": ST+r"\atlas-pair\reference_labeled.h5ad", "mono": ST+r"\atlas-pair-holdout\reference_no_monocytes.h5ad",
       "bcell": ST+r"\atlas-pair-holdout\reference_no_bcells.h5ad"}[case]
w = os.path.join(RUN, "work", tag); shutil.rmtree(w, ignore_errors=True); os.makedirs(w); os.chdir(w)
shutil.copy(ref, "reference_labeled.h5ad"); shutil.copy(ST+r"\atlas-pair\query.h5ad", "query.h5ad")
g = runpy.run_path(SK + r"\scripts\scarches_annotation.py")
q = g['adata_query']; pred = q.obs['predicted_label'].astype(str); truth = q.obs['truth_coarse'].astype(str)
drop = {"none": None, "mono": "Monocytes", "bcell": "B cells"}[case]
m = (truth == drop) if drop else np.ones(len(q), bool)
out = {"case": case, "n_target": int(m.sum()), "pct_unknown_knn_gate": float((pred[m] == 'Unknown').mean()),
       "top_pred": pred[m].value_counts().head(4).to_dict(),
       "query_annotated_sha256": hashlib.sha256(open("query_annotated.h5ad","rb").read()).hexdigest()}
py = sys.executable
for mk, args in (("curated", ["--markers", SK + r"\references\pbmc-markers.json"]), ("derived", [])):
    r = subprocess.run([py, SK + r"\scripts\label_marker_check.py", "--out", f"marker_{mk}.tsv"] + args, capture_output=True, text=True)
    out["marker_"+mk] = r.stdout.strip().splitlines()[-12:] ; out["marker_"+mk+"_rc"] = r.returncode
json.dump(out, open(os.path.join(RUN, f"summary_{tag}.json"), "w"), indent=1); print(json.dumps(out, indent=1))
