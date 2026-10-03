"""Two checks on SKILL.md statements, synthetic with known truth (seeded).
(1) p>>n: the Skill's CoxnetSurvivalAnalysis(l1_ratio=0.9, alpha_min_ratio=0.01, fit_baseline_model=True) snippet calls predict() with the
    default alpha (smallest on the path). Compare held-out Uno C and number of nonzero coefficients against a CV-selected alpha.
(2) 'Harrell's C is biased upward under heavy censoring': compare Harrell and Uno estimates with the uncensored truth under light vs
    heavy random (covariate-dependent) censoring."""
import warnings
import numpy as np
from sksurv.util import Surv
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw
from sklearn.model_selection import GridSearchCV, KFold
warnings.filterwarnings("ignore")
rng = np.random.default_rng(1)
# (1) n=150 train, p=1000 (5 prognostic), 600 test
def sim(n, p=1000):
    X = rng.normal(size=(n, p)); lin = X[:, :5] @ np.full(5, 0.7)
    t = rng.exponential(np.exp(-lin)); c = rng.exponential(2.0, n)
    return X, Surv.from_arrays(t <= c, np.minimum(t, c)), lin
Xtr, ytr, _ = sim(150); Xte, yte, lin_te = sim(600)
m = CoxnetSurvivalAnalysis(l1_ratio=0.9, alpha_min_ratio=0.01, fit_baseline_model=True).fit(Xtr, ytr)
tau = np.percentile(yte['time'][yte['event']], 80)
print(f"path: {len(m.alphas_)} alphas, alpha_max {m.alphas_[0]:.3f}, alpha_min {m.alphas_[-1]:.3f}")
for name, a in (("default predict() = smallest alpha", m.alphas_[-1]), ("alpha_max/2 (sparser)", m.alphas_[len(m.alphas_) // 2])):
    nz = int((m.coef_[:, np.argmin(abs(m.alphas_ - a))] != 0).sum())
    print(f"{name:38s} nonzero {nz:4d}  held-out Uno C {concordance_index_ipcw(ytr, yte, m.predict(Xte, alpha=a), tau=tau)[0]:.3f}")
gs = GridSearchCV(CoxnetSurvivalAnalysis(l1_ratio=0.9), {"alphas": [[a] for a in m.alphas_[::4]]}, cv=KFold(5, shuffle=True, random_state=0)).fit(Xtr, ytr)
b = gs.best_estimator_
print(f"CV-selected alpha {b.alphas_[0]:.3f}               nonzero {int((b.coef_ != 0).sum()):4d}  held-out Uno C {concordance_index_ipcw(ytr, yte, b.predict(Xte), tau=tau)[0]:.3f}")
print("oracle (true linear predictor) held-out Uno C", round(concordance_index_ipcw(ytr, yte, lin_te, tau=tau)[0], 3))
# (2) Harrell vs Uno vs truth
def trial(cens_scale, n=3000):
    X = rng.normal(size=(n, 2)); lin = 0.8 * X[:, 0] + 0.5 * X[:, 1]
    t = rng.exponential(np.exp(-lin)); c = rng.exponential(cens_scale * np.exp(0.4 * X[:, 0]))   # censoring depends on covariate (informative via X)
    y = Surv.from_arrays(t <= c, np.minimum(t, c)); y0 = Surv.from_arrays(np.ones(n, bool), t)
    tau_ = np.percentile(y['time'][y['event']], 90)
    return (1 - y['event'].mean(), concordance_index_censored(y0['event'], y0['time'], lin)[0],
            concordance_index_censored(y['event'], y['time'], lin)[0], concordance_index_ipcw(y, y, lin, tau=tau_)[0])
print(f"{'censored':>9} {'truth C':>8} {'Harrell':>8} {'Uno(tau)':>9}   (mean of 5 reps)")
for scale in (20.0, 1.0, 0.25):
    r = np.mean([trial(scale) for _ in range(5)], axis=0)
    print(f"{r[0]:9.2f} {r[1]:8.3f} {r[2]:8.3f} {r[3]:9.3f}")
