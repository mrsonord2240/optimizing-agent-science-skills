"""Does scArches surgery leave the reference weights unchanged? (checks 'without retraining the reference')"""
import os, sys, torch, numpy as np, scanpy as sc, scvi
scvi.settings.seed = 0
D = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\atlas-pair"
ref = sc.read_h5ad(os.path.join(D, "reference_labeled.h5ad")); q = sc.read_h5ad(os.path.join(D, "query.h5ad"))
out = os.path.join(os.environ.get("RUN"), "work"); os.makedirs(out, exist_ok=True); os.chdir(out)
scvi.model.SCVI.setup_anndata(ref, layer="counts", batch_key="batch")
m = scvi.model.SCVI(ref, n_latent=10, n_layers=1); m.train(max_epochs=15, accelerator="cpu")
m.save("refm", overwrite=True, save_anndata=True)
before = {k: v.detach().clone() for k, v in m.module.state_dict().items()}
scvi.model.SCVI.prepare_query_anndata(q, "refm")
qm = scvi.model.SCVI.load_query_data(q, "refm")
loaded = {k: v.detach().clone() for k, v in qm.module.state_dict().items()}
qm.train(max_epochs=15, plan_kwargs={"weight_decay": 0.0}, accelerator="cpu")
after = qm.module.state_dict()
tr = [n for n, p in qm.module.named_parameters() if p.requires_grad]
print("trainable params after load_query_data:", tr)
chg, same = [], []
for k, v in after.items():
    if k in before and before[k].shape == v.shape:
        (same if torch.equal(before[k], v) else chg).append(k)
    else: chg.append(k + " (shape/new)")
print("unchanged tensors:", len(same)); print("changed/new tensors:", chg)
# reference object itself untouched in memory and on disk
print("ref model object unchanged:", all(torch.equal(before[k], v) for k, v in m.module.state_dict().items()))
m2 = scvi.model.SCVI.load("refm", adata=ref)
print("saved ref reloads identical:", all(torch.equal(before[k], v) for k, v in m2.module.state_dict().items()))
