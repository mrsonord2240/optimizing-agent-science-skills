"""Re-audit SA-002: Coxnet alpha selected on training data only. By construction (signature + data-flow trace) and by test
(replace/permute the TEST set: alpha and coefficients must be bit-identical; change the TRAIN set: they must change = positive control).
Also the SKILL.md fitting snippet is exercised with a corrupted test partition."""
import sys, os, re, inspect, hashlib, warnings, numpy as np
sys.dont_write_bytecode = True
SKD = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis"
sys.path.insert(0, SKD + r"\scripts"); import cox_regression as cr
from sksurv.util import Surv
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sklearn.model_selection import train_test_split
warnings.simplefilter("ignore")
print("fit_coxnet_cv signature:", inspect.signature(cr.fit_coxnet_cv))
assert not any(k in inspect.signature(cr.fit_coxnet_cv).parameters for k in ("X_test", "y_test", "X_val", "y_val"))

def rowhash(a): return {hashlib.sha1(np.ascontiguousarray(r).tobytes()).hexdigest() for r in a}
def trace(X_train, y_train, X_test):
    """Record every X passed to Coxnet.fit / predict during fit_coxnet_cv; none may contain a test row."""
    seen = []
    class Spy(CoxnetSurvivalAnalysis):
        def fit(self, X, y, *a, **k): seen.append(("fit", rowhash(X))); return super().fit(X, y, *a, **k)
        def predict(self, X, *a, **k): seen.append(("predict", rowhash(X))); return super().predict(X, *a, **k)
    orig = cr.CoxnetSurvivalAnalysis; cr.CoxnetSurvivalAnalysis = Spy
    try: m = cr.fit_coxnet_cv(X_train, y_train)
    finally: cr.CoxnetSurvivalAnalysis = orig
    tr, te = rowhash(X_train), rowhash(X_test)
    leaks = sum(len(h & (te - tr)) for _, h in seen); outside = sum(len(h - tr) for _, h in seen)
    return m, len(seen), leaks, outside

def run(name, Xtr, ytr, Xte, yte):
    rng = np.random.default_rng(1)
    m0, ncalls, leaks, outside = trace(Xtr, ytr, Xte)
    print(f"[{name}] fit/predict calls inside fit_coxnet_cv: {ncalls}; rows outside the training set: {outside}; test-only rows seen: {leaks}")
    assert leaks == 0 and outside == 0
    a0, c0 = m0.alphas_[0], m0.coef_.copy()
    # perturbations of the TEST set only (fit_coxnet_cv cannot see it, but run the whole chain to be explicit)
    for label, (Xt2, yt2) in {
        "test permuted": (Xte[rng.permutation(len(Xte))], yte[rng.permutation(len(yte))]),
        "test replaced by noise/random labels": (rng.normal(size=Xte.shape), Surv.from_arrays(rng.random(len(yte)) < .5, rng.exponential(1, len(yte)))),
        "test emptied to 5 rows": (Xte[:5], yte[:5]),
    }.items():
        m1 = cr.fit_coxnet_cv(Xtr, ytr)      # no test argument exists; call again after the test set was changed
        same = (m1.alphas_[0] == a0) and np.array_equal(m1.coef_, c0)
        print(f"   {label}: alpha {m1.alphas_[0]:.6f} vs {a0:.6f}; coef identical: {np.array_equal(m1.coef_, c0)}")
        assert same
    # positive control: changing TRAIN changes the selection
    idx = rng.permutation(len(ytr))[: int(0.7 * len(ytr))]
    m2 = cr.fit_coxnet_cv(Xtr[idx], ytr[idx])
    print(f"   positive control (70% of train): alpha {m2.alphas_[0]:.6f} nonzero {(m2.coef_!=0).sum()} vs {(c0!=0).sum()}")
    assert m2.alphas_[0] != a0 or not np.array_equal(m2.coef_, c0)
    return a0, int((c0 != 0).sum())

X, y = cr.load_data('gbsg2'); Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y['event'])
print("GBSG2:", run("GBSG2", Xtr, ytr, Xte, yte))
z = np.load(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\survival-pgtn\pgtn.npz")
Xtr, Xte = z["X_train"], z["X_test"]; ytr = Surv.from_arrays(z["event_train"], z["time_train"]); yte = Surv.from_arrays(z["event_test"], z["time_test"])
print("p>>n:", run("p>>n n=150 p=1000", Xtr, ytr, Xte, yte))

# SKILL.md fitting snippet with a corrupted test partition: alpha and coefs must not move.
s = open(SKD + r"\SKILL.md", encoding="utf-8").read()
blocks = re.findall(r"```python\n(.*?)```", s, re.S); fit_block = blocks[0]
def exec_fit(corrupt):
    import sklearn.model_selection as ms
    real = ms.train_test_split
    def patched(X, y, **k):
        a, b, c, d = real(X, y, **k)
        if corrupt:
            r = np.random.default_rng(7); b = r.normal(size=b.shape) * 50; d = d[r.permutation(len(d))]
        return a, b, c, d
    g = {}
    ms.train_test_split = patched
    try:
        exec(compile(fit_block.replace("risk = coxnet.predict(X_test)", "risk = None"), "SKILL.md-fit-block", "exec"), g)
    finally: ms.train_test_split = real
    return g["coxnet"].alphas_[0], g["coxnet"].coef_.copy()
a1, c1 = exec_fit(False); a2, c2 = exec_fit(True)
print(f"SKILL.md fit block: clean-test alpha {a1:.6f}, corrupted-test alpha {a2:.6f}, coef identical {np.array_equal(c1,c2)}")
assert a1 == a2 and np.array_equal(c1, c2)
print("PASS SA-002 by construction and test")
