"""Audit check (SYNTHETIC planted-truth fixture on REAL hg38-derived backgrounds).
Skill method-reference: y_ref,y_alt = substitution_effect(model,X,subs); log2fc = np.log2(y_alt.sum(-1)/y_ref.sum(-1)).
chromBPNet/BPNet heads: profile logits + LOG-counts. Test whether the Skill formula equals the true count log2FC
(log2(exp(y_alt)/exp(y_ref)) = (y_alt-y_ref)/ln2) when applied to the log-count head, and what happens with the raw (profile,counts) tuple.
Run: source env.sh; py_torch audit_log2fc_formula.py OUT.json"""
import sys, json, numpy as np, torch
src = open('/mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/smoke_torch_tools.py').read()
head = src.split("# ---- bpnet-lite: train")[0]
head = head.replace('OUT = sys.argv[1]\nos.makedirs(OUT, exist_ok=True)', 'OUT="/tmp"')
exec(head)
from bpnetlite.bpnet import BPNet, CountWrapper
from tangermeme.variant_effect import substitution_effect
torch.manual_seed(0)
m = BPNet(n_filters=32, n_layers=4, n_outputs=1, n_control_tracks=0, trimming=(L - 1000) // 2, verbose=False).to(dev)
opt = torch.optim.Adam(m.parameters(), lr=3e-3)
for ep in range(60):
    perm = torch.randperm(len(Xtr))
    for b in range(0, len(Xtr), 64):
        ix = perm[b:b + 64]; x, p, c = Xtr[ix].to(dev), Ptr[ix].to(dev), Ctr[ix].to(dev)
        yp, yc = m(x)
        lp = (-(torch.nn.functional.log_softmax(yp.flatten(1), -1) * p.flatten(1)).sum(-1) / p.flatten(1).sum(-1)).mean()
        (lp + 10 * torch.nn.functional.mse_loss(yc, c)).backward(); opt.step(); opt.zero_grad()
m.eval()
cw = CountWrapper(m).to(dev).eval()
ix = np.where(plant_te >= 0)[0][:40]
subs = torch.tensor([[j, int(plant_te[i]) + 3, 0] for j, i in enumerate(ix)])
r = substitution_effect(cw, Xte[ix], subs, device=dev, verbose=False)
y_ref, y_alt = r
skill = np.log2(np.asarray(y_alt.sum(axis=-1) / y_ref.sum(axis=-1)))
true = np.asarray((y_alt - y_ref).squeeze() / np.log(2))
out = {"y_ref_mean_logcount": float(y_ref.mean()), "skill_formula_mean": float(np.mean(skill)),
       "true_log2fc_mean": float(np.mean(true)), "ratio_true_over_skill": float(np.mean(true) / np.mean(skill)),
       "skill_vs_true_spearman": float(__import__('scipy.stats').stats.spearmanr(skill.ravel(), true.ravel())[0]) if True else None,
       "n": int(len(skill))}
try:
    r2 = substitution_effect(m, Xte[ix], subs, device=dev, verbose=False)
    a, b = r2
    out["raw_bpnet_output_types"] = [type(a).__name__, type(b).__name__]
    try:
        np.log2(b.sum(axis=-1) / a.sum(axis=-1)); out["raw_tuple_skill_formula"] = "ran"
    except Exception as e:
        out["raw_tuple_skill_formula"] = "ERR " + repr(e)[:160]
except Exception as e:
    out["raw_bpnet_output_types"] = "ERR " + repr(e)[:200]
print(json.dumps(out, indent=1)); json.dump(out, open(sys.argv[1], 'w'), indent=1)
