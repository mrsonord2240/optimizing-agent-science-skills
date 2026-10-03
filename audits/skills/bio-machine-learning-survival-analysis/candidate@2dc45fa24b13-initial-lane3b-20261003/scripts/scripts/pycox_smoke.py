# pycox (named in survival-analysis prose: DeepSurv / DeepHit / compute_baseline_hazards) on real GBSG2 (bundled in scikit-survival).
import numpy as np, torch, torchtuples as tt
from sksurv.datasets import load_gbsg2
from sksurv.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from pycox.models import CoxPH, DeepHitSingle
from pycox.evaluation import EvalSurv

torch.manual_seed(0); np.random.seed(0)
X, y = load_gbsg2()
Xn = OneHotEncoder().fit_transform(X).astype('float32')
dur = y['time'].astype('float32'); ev = y['cens'].astype('float32')
Xtr, Xte, dtr, dte, etr, ete = train_test_split(Xn.values, dur, ev, test_size=0.3, random_state=0, stratify=ev)
sc = StandardScaler().fit(Xtr); Xtr, Xte = sc.transform(Xtr).astype('float32'), sc.transform(Xte).astype('float32')

# DeepSurv (CoxPH); baseline hazards must be computed before predict_surv_df (SKILL.md failure-mode row)
net = tt.practical.MLPVanilla(Xtr.shape[1], [32, 32], 1, batch_norm=True, dropout=0.1, output_bias=False)
model = CoxPH(net, tt.optim.Adam(0.01))
model.fit(Xtr, (dtr, etr), batch_size=64, epochs=30, verbose=False)
model.compute_baseline_hazards()
surv = model.predict_surv_df(Xte)
c = EvalSurv(surv, dte, ete, censor_surv='km').concordance_td('antolini')
print(f"DeepSurv (pycox CoxPH) test C-td {c:.3f}, surv_df {surv.shape}")
assert 0.55 < c < 0.85

# DeepHit (single risk) with discretised time
labtrans = DeepHitSingle.label_transform(20)
ytr = labtrans.fit_transform(dtr, etr)
net2 = tt.practical.MLPVanilla(Xtr.shape[1], [32, 32], labtrans.out_features, batch_norm=True, dropout=0.1)
dh = DeepHitSingle(net2, tt.optim.Adam(0.01), alpha=0.2, sigma=0.1, duration_index=labtrans.cuts)
dh.fit(Xtr, ytr, batch_size=64, epochs=30, verbose=False)
c2 = EvalSurv(dh.predict_surv_df(Xte), dte, ete, censor_surv='km').concordance_td('antolini')
print(f"DeepHit test C-td {c2:.3f}")
assert 0.5 < c2 < 0.85
