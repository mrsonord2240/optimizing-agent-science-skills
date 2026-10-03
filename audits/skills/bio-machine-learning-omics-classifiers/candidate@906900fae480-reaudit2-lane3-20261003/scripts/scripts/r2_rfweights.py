"""OC-007 independent generator (own coefficients/seeds, not the staged exp_rf_weights.py).
Usage: python r2_rfweights.py   Two setups: A p=60 k=10 n=1500 ~8%; B p=200 k=15 n=800 ~15%. Plain vs balanced: logistic and RF, test AUC and risk ratio. 6 seeds each."""
import warnings, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
warnings.simplefilter('error', FutureWarning)
def run(P, K, ntr, icpt, scale, tag):
    beta = np.zeros(P); beta[:K] = np.random.default_rng(4242).normal(scale=scale, size=K)
    out = []
    for s in range(6):
        r = np.random.default_rng(9000 + s)
        def gen(n):
            X = r.normal(size=(n, P)); return X, (r.random(n) < 1/(1+np.exp(-(X@beta+icpt)))).astype(int)
        Xtr, ytr = gen(ntr); Xte, yte = gen(15000)
        row = [yte.mean()]
        for cw in (None, 'balanced'):
            lr = LogisticRegression(C=0.1, max_iter=5000, class_weight=cw).fit(Xtr, ytr); p = lr.predict_proba(Xte)[:, 1]
            row += [roc_auc_score(yte, p), p.mean()/yte.mean()]
        for cw in (None, 'balanced'):
            rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight=cw, random_state=0, n_jobs=4).fit(Xtr, ytr); p = rf.predict_proba(Xte)[:, 1]
            row += [roc_auc_score(yte, p), p.mean()/yte.mean()]
        out.append(row); print(tag, s, np.round(row, 3), flush=True)
    a = np.array(out)
    print(f'{tag} MEAN prev {a[:,0].mean():.3f} | LR auc plain {a[:,1].mean():.3f} bal {a[:,3].mean():.3f} ratio {a[:,2].mean():.2f}/{a[:,4].mean():.2f} | RF auc plain {a[:,5].mean():.3f} bal {a[:,7].mean():.3f} (bal>plain in {(a[:,7]>a[:,5]).sum()}/6) ratio {a[:,6].mean():.2f}/{a[:,8].mean():.2f}')
run(60, 10, 1500, -3.4, 0.7, 'A')
run(200, 15, 800, -2.2, 0.6, 'B')
