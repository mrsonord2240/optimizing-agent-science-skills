"""Input 6 (Scope boundary) -- a confirmatory trial with 4 pre-specified endpoints.
SKILL.md routes this to clinical-biostatistics/multiplicity-graphical. Before handing
off, the central claim behind that routing is checked: FDR control is NOT FWER control
when the family is small. SYNTHETIC: 200000 trials under the GLOBAL NULL, 4 endpoints
correlated at rho=0.3. BH / Holm / Bonferroni / Hochberg implemented vectorised."""
import numpy as np
from scipy import stats
RNG = np.random.default_rng(1122)
K, TRIALS, ALPHA, rho = 4, 200000, 0.05, 0.3
L = np.linalg.cholesky(rho*np.ones((K, K)) + (1-rho)*np.eye(K))
z = (L @ RNG.normal(size=(K, TRIALS))).T          # TRIALS x K, global null
p = np.sort(2*stats.norm.sf(np.abs(z)), axis=1)
i = np.arange(1, K+1)
bh    = (p <= ALPHA*i/K).any(1)                              # Benjamini-Hochberg
holm  = (p[:, 0] <= ALPHA/K)                                 # Holm rejects >=1 iff p(1)<=a/K
bonf  = (p[:, 0] <= ALPHA/K)
hoch  = (p <= ALPHA/(K - i + 1)).any(1)                      # Hochberg
raw   = (p[:, 0] <= ALPHA)
print(f"SYNTHETIC global null, {K} correlated endpoints (rho={rho}), {TRIALS} trials, alpha={ALPHA}")
print(f"{'procedure':14s} {'family-wise type I error':>26s}")
for name, r in (("none", raw), ("BH (FDR)", bh), ("Holm", holm),
                ("Bonferroni", bonf), ("Hochberg", hoch)):
    print(f"{name:14s} {r.mean():26.4f}")
print("FWER target is 0.05. Under the global null FDR == FWER in theory; the gap that")
print("matters appears once some endpoints are true, so the same check is repeated with")
print("2 of 4 endpoints truly non-null (shift 3.0):")
mu = np.array([3.0, 3.0, 0.0, 0.0])
z2 = (L @ RNG.normal(size=(K, TRIALS))).T + mu
p2 = 2*stats.norm.sf(np.abs(z2))
order = np.argsort(p2, axis=1)
ps = np.take_along_axis(p2, order, axis=1)
null_mask = np.take_along_axis(np.tile(mu == 0, (TRIALS, 1)), order, axis=1)
bh_rej = np.zeros_like(ps, bool)
kmax = (ps <= ALPHA*i/K)
last = np.where(kmax.any(1), K - 1 - np.argmax(kmax[:, ::-1], axis=1), -1)
for r_ in range(K):
    bh_rej[:, r_] = r_ <= last
holm_rej = np.zeros_like(ps, bool)
passing = ps <= ALPHA/(K - i + 1)
stop = np.where(~passing.all(1), np.argmin(passing, axis=1), K)
for r_ in range(K):
    holm_rej[:, r_] = r_ < stop
print(f"{'BH (FDR)':14s} FWER among the 2 true nulls: {(bh_rej & null_mask).any(1).mean():.4f}")
print(f"{'Holm':14s} FWER among the 2 true nulls: {(holm_rej & null_mask).any(1).mean():.4f}")
