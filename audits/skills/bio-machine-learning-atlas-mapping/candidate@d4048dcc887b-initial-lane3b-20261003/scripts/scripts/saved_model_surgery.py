"""SKILL.md snippets 1-3 via saved-model directories (the route scarches_annotation.py does not take) plus checks on
predict(soft=True): return type, columns, row sums, agreement with predict(), and what the documented softmax-max reading returns.
Reduced epochs (CPU). Inputs: derived atlas pair (PBMC 1k v3 reference w/ CellTypist labels, PBMC3k query)."""
import os, shutil, numpy as np, pandas as pd, scanpy as sc, scvi
from sklearn.neighbors import KNeighborsClassifier
D = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\atlas-pair"
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "saved_model"); W = os.path.abspath(W)
shutil.rmtree(W, ignore_errors=True); os.makedirs(W); os.chdir(W)
scvi.settings.seed = 0
print("scvi-tools", scvi.__version__)
ref = sc.read_h5ad(os.path.join(D, "reference_labeled.h5ad"))
scvi.model.SCVI.setup_anndata(ref, layer='counts', batch_key='batch')
ref_vae = scvi.model.SCVI(ref, n_latent=30, n_layers=2); ref_vae.train(max_epochs=30, accelerator='cpu')
ref_vae.save('reference_model/', save_anndata=True)
# snippet 1: scVI surgery from saved dir
q = sc.read_h5ad(os.path.join(D, "query.h5ad"))
scvi.model.SCVI.prepare_query_anndata(q, 'reference_model/')
qm = scvi.model.SCVI.load_query_data(q, 'reference_model/')
qm.train(max_epochs=30, plan_kwargs={'weight_decay': 0.0}, check_val_every_n_epoch=10, accelerator='cpu')
q.obsm['X_scVI'] = qm.get_latent_representation(); print("scVI query latent", q.obsm['X_scVI'].shape)
# snippet 2: scANVI head, save, surgery from dir
rs = scvi.model.SCANVI.from_scvi_model(ref_vae, unlabeled_category='Unknown', labels_key='cell_type')
rs.train(max_epochs=20, n_samples_per_label=100, accelerator='cpu'); rs.save('ref_scanvi/', save_anndata=True)
q2 = sc.read_h5ad(os.path.join(D, "query.h5ad"))
scvi.model.SCANVI.prepare_query_anndata(q2, 'ref_scanvi/')
qs = scvi.model.SCANVI.load_query_data(q2, 'ref_scanvi/')
qs.train(max_epochs=30, plan_kwargs={'weight_decay': 0.0}, accelerator='cpu')
q2.obs['predicted_label'] = qs.predict(); q2.obsm['X_scANVI'] = qs.get_latent_representation()
proba = qs.predict(soft=True)
print("== predict(soft=True) ==")
print("type:", type(proba).__name__, "shape:", proba.shape)
print("columns:", list(getattr(proba, 'columns', [])))
print("row sums min/max:", float(np.asarray(proba).sum(1).min()), float(np.asarray(proba).sum(1).max()))
print("idxmax(axis=1) == predict():", bool((proba.idxmax(axis=1).values == q2.obs['predicted_label'].values).mean() > 0.999))
print("proba.max() ->", type(proba.max()).__name__, "(per-class column maxima, len %d); proba.max(axis=1) -> per-cell vector len %d" % (len(proba.max()), len(proba.max(axis=1))))
print("proba[:, 0] raises:", end=" ")
try:
    proba[:, 0]; print("no")
except Exception as e:
    print(type(e).__name__)
# snippet 3: kNN OOD gate
knn = KNeighborsClassifier(n_neighbors=15, weights='distance').fit(rs.get_latent_representation(), ref.obs['cell_type'])
unc = 1.0 - knn.predict_proba(q2.obsm['X_scANVI']).max(axis=1)
q2.obs.loc[unc > 0.2, 'predicted_label'] = 'Unknown'
t = q2.obs['truth_coarse'].astype(str); p = q2.obs['predicted_label'].astype(str)
print(f"flagged Unknown {(unc > 0.2).mean():.1%}  accuracy vs PBMC3k annotation {(t == p).mean():.3f}")
assert (t == p).mean() > 0.8
