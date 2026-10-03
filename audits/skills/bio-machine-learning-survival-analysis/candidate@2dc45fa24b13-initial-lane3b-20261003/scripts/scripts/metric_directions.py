"""Metric-direction traps on GBSG2 (686 pts), held-out split: sksurv Harrell/Uno C vs lifelines C (sign), Uno vs Harrell under added censoring."""
import numpy as np
from sksurv.datasets import load_gbsg2
from sksurv.preprocessing import OneHotEncoder
from sksurv.util import Surv
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw
from sklearn.model_selection import train_test_split
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
X, y = load_gbsg2(); Xn = OneHotEncoder().fit_transform(X).astype(float)
Xtr, Xte, ytr, yte = train_test_split(Xn, y, test_size=0.3, random_state=0, stratify=y['cens'])
S = lambda a: Surv.from_arrays(a['cens'].astype(bool), a['time'].astype(float))
a, b = S(ytr), S(yte)
df = Xtr.copy(); df['time'] = ytr['time'].astype(float); df['event'] = ytr['cens'].astype(int)
cph = CoxPHFitter(penalizer=0.01).fit(df, 'time', 'event')
ph = cph.predict_partial_hazard(Xte).values
print("lifelines C on HELD-OUT: +ph", round(concordance_index(yte['time'], ph, yte['cens']), 3), " -ph", round(concordance_index(yte['time'], -ph, yte['cens']), 3))
print("sksurv Harrell C (risk=ph):", round(concordance_index_censored(b['event'], b['time'], ph)[0], 3), " (risk=-ph):", round(concordance_index_censored(b['event'], b['time'], -ph)[0], 3))
tau = np.percentile(a['time'][a['event']], 90)
print("sksurv Uno C (risk=ph):", round(concordance_index_ipcw(a, b, ph, tau=tau)[0], 3), " (risk=-ph):", round(concordance_index_ipcw(a, b, -ph, tau=tau)[0], 3))
cut = np.percentile(yte['time'], 40)
t2 = np.minimum(yte['time'], cut); e2 = yte['cens'] & (yte['time'] <= cut)
b2 = Surv.from_arrays(e2.astype(bool), t2.astype(float))
tau2 = min(tau, cut * 0.999)
print(f"heavy administrative censoring of test set (cut {cut:.0f} d, events {int(e2.sum())}/{len(e2)}): Harrell {concordance_index_censored(b2['event'], b2['time'], ph)[0]:.3f}  Uno(tau={tau2:.0f}) {concordance_index_ipcw(a, b2, ph, tau=tau2)[0]:.3f}")
