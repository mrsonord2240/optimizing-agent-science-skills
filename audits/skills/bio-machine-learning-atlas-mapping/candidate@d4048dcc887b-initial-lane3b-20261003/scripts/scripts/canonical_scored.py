"""Canonical workflow: run the Skill's scarches_annotation.py UNMODIFIED (runpy) on the PBMC reference/query pair and score it.
Reference = 10x PBMC 1k v3 with CellTypist (silver) labels; query = PBMC3k (10x v1), truth = PBMC3k louvain annotation mapped to coarse classes.
Usage: canonical_scored.py <tag>   (run twice with different tags to measure run-to-run variation; script sets no seed)"""
import os, sys, shutil, runpy, json
import pandas as pd
PAIR = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\atlas-pair"
SKILL = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping\scripts\scarches_annotation.py"
tag = sys.argv[1]
w = os.path.join(os.getcwd(), "canon_" + tag); shutil.rmtree(w, ignore_errors=True); os.makedirs(w); os.chdir(w)
for f in ("reference_labeled.h5ad", "query.h5ad"):
    shutil.copy(os.path.join(PAIR, f), f)
g = runpy.run_path(SKILL)
q = g['adata_query']; t = q.obs['truth_coarse'].astype(str); p = q.obs['predicted_label'].astype(str)
ct = pd.crosstab(t, p)
print(ct.to_string())
res = {"tag": tag, "acc_all": float((t == p).mean()), "unknown_pct": float((p == 'Unknown').mean()),
       "acc_non_unknown": float((t[p != 'Unknown'] == p[p != 'Unknown']).mean()),
       "mean_unc_correct": float(q.obs.loc[t == p, 'transfer_uncertainty'].mean()),
       "mean_unc_wrong": float(q.obs.loc[t != p, 'transfer_uncertainty'].mean()),
       "outputs_written_by_script": sorted(os.listdir("."))}
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(os.path.dirname(w), f"canonical_{tag}.json"), "w"), indent=1)
