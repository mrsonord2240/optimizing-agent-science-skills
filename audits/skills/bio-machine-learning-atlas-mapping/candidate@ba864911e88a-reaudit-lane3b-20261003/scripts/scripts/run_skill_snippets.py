"""Execute the three python blocks of SKILL.md (scVI surgery, scANVI transfer, kNN gate) AS WRITTEN, in order, via exec.
Prelude only supplies what the text says the user already has: reference_model/ (saved scVI), adata_ref, query.h5ad.
Epochs are NOT reduced. Usage: run_skill_snippets.py <workdir>"""
import os, re, sys, shutil, time, json
ST = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\atlas-pair"
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping\SKILL.md"
w = sys.argv[1]; shutil.rmtree(w, ignore_errors=True); os.makedirs(w); os.chdir(w)
shutil.copy(ST + r"\query.h5ad", "query.h5ad")
md = open(SK, encoding='utf-8').read()
blocks = re.findall(r"```python\n(.*?)```", md, re.S)
print("python blocks:", len(blocks))
import scvi, scanpy as sc, numpy as np
scvi.settings.seed = 0
# prelude: a "saved reference scVI" as snippet 1 assumes
ref = sc.read_h5ad(ST + r"\reference_labeled.h5ad")
scvi.model.SCVI.setup_anndata(ref, layer='counts', batch_key='batch')
m = scvi.model.SCVI(ref, n_latent=30, n_layers=2); m.train(max_epochs=100, early_stopping=True)
m.save('reference_model/', save_anndata=True, overwrite=True)
g = {}
g['adata_ref'] = sc.read_h5ad(ST + r"\reference_labeled.h5ad")   # snippet 2 says: counts in layers['counts'], obs cell_type/batch
for i, b in enumerate(blocks[:3], 1):
    t = time.time(); print(f"--- block {i} ---", flush=True)
    exec(compile(b, f"SKILL_block{i}", "exec"), g)
    print(f"block {i} ok {time.time()-t:.0f}s", flush=True)
q = g['adata_query']; proba = g['proba']
res = dict(latent_scVI=list(q.obsm['X_scVI'].shape), latent_scANVI=list(q.obsm['X_scANVI'].shape), proba_type=type(proba).__name__,
           proba_shape=list(proba.shape), rows_sum_to_1=bool(np.allclose(proba.sum(axis=1), 1, atol=1e-3)),
           unknown_frac=float((q.obs['predicted_label'] == 'Unknown').mean()))
tr = sc.read_h5ad(ST + r"\query.h5ad").obs['truth_coarse'].astype(str).values
p = q.obs['predicted_label'].astype(str).values
res['acc_vs_truth_all'] = float((p == tr).mean()); ok = p != 'Unknown'; res['acc_nonunknown'] = float((p[ok] == tr[ok]).mean())
print(json.dumps(res, indent=1)); json.dump(res, open('snippets_result.json', 'w'), indent=1)
