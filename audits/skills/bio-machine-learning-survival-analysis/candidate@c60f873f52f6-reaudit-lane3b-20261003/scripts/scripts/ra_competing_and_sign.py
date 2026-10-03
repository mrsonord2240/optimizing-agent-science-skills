"""Re-audit: competing-risks claims (hand table vs lifelines AJ vs sksurv; 1-KM >= CIF), unchanged-bytes check for
scripts/competing_risks_cif.py + references/failure-modes.md, lifelines concordance sign trap (1-C), tie warning."""
import sys, hashlib, json, warnings, numpy as np
sys.dont_write_bytecode = True
SKD = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis"
INIT = r"F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-survival-analysis\candidate@2dc45fa24b13-initial-lane3b-20261003\source-identity.json"
print("== unchanged bytes vs the audited (initial) identity")
rec = {f["path"]: f["sha256"] for f in json.load(open(INIT))["files"]}
for p in ("scripts/competing_risks_cif.py", "references/failure-modes.md"):
    h = hashlib.sha256(open(SKD + "\\" + p.replace("/", "\\"), "rb").read()).hexdigest()
    print(f"  {p}: current {h[:16]} audited {rec[p][:16]} -> {'IDENTICAL' if h == rec[p] else 'CHANGED'}"); assert h == rec[p]
from lifelines import KaplanMeierFitter, AalenJohansenFitter
from sksurv.nonparametric import cumulative_incidence_competing_risks as cicr
print("== hand table: (t,cause) (1,1)(2,2)(3,1)(4,0 censored)(5,2)")
t = np.array([1, 2, 3, 4, 5.]); c = np.array([1, 2, 1, 0, 2])
# AJ by hand: S: 1 ->0.8 (t1) ->0.6 (t2) ->0.4 (t3); CIF1 = 0.2, 0.2, 0.4, 0.4, 0.4 ; CIF2 = 0, .2, .2, .2, .6 ; 1-KM(c2 censored): 0.2,0.2,0.4667
hand1 = {1: .2, 2: .2, 3: .4, 4: .4, 5: .4}; hand2 = {1: 0, 2: .2, 3: .2, 4: .2, 5: .6}; hand_1km = {1: .2, 2: .2, 3: 1 - .8 * 2 / 3, 4: 1 - .8 * 2 / 3, 5: 1 - .8 * 2 / 3}
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    aj = AalenJohansenFitter(calculate_variance=False).fit(t, c, event_of_interest=1)
print("  lifelines warnings on this (tie-free) table:", [str(x.message)[:60] for x in w] or "none")
km = KaplanMeierFitter().fit(t, c == 1)
ts, cif = cicr(c.astype(int), t)[0], cicr(c.astype(int), t)[1]
for h in (1, 2, 3, 4, 5):
    a = float(aj.cumulative_density_.loc[:h].iloc[-1, 0]); k = 1 - float(km.predict(h)); i = ts.searchsorted(h, side='right') - 1
    s1, s2 = cif[1][i], cif[2][i]
    print(f"  t={h}: hand CIF1 {hand1[h]:.4f} lifelines AJ {a:.4f} sksurv {s1:.4f} | hand CIF2 {hand2[h]:.4f} sksurv {s2:.4f} | hand 1-KM {hand_1km[h]:.4f} lifelines 1-KM {k:.4f}")
    assert abs(a - hand1[h]) < 1e-12 and abs(s1 - hand1[h]) < 1e-12 and abs(s2 - hand2[h]) < 1e-12 and abs(k - hand_1km[h]) < 1e-12
    assert k >= a - 1e-12                      # the Skill's stated inequality
print("  row0 (all causes) at t=5:", cif[0][-1], "(= 0.4+0.6 = 1.0 expected)"); assert abs(cif[0][-1] - 1.0) < 1e-12
print("  PASS hand table: lifelines AJ == sksurv == hand; 1-KM >= CIF everywhere (strict at t=3: 0.4667 vs 0.4)")
print("== script data (seed 0, n=3000): lifelines AJ vs sksurv over a grid, and 1-KM >= CIF")
rng = np.random.default_rng(0); n = 3000
t1 = rng.exponential(4.0, n); t2 = rng.exponential(1.5, n); admin = rng.uniform(0, 8, n)
time = np.minimum.reduce([t1, t2, admin]); cause = np.where((t1 <= t2) & (t1 <= admin), 1, np.where((t2 < t1) & (t2 <= admin), 2, 0))
ajf = AalenJohansenFitter().fit(time, cause, event_of_interest=1); km = KaplanMeierFitter().fit(time, cause == 1)
ts, cf = cicr(cause.astype(int), time)
mx = 0; viol = 0
for h in np.linspace(0.1, 7.5, 40):
    a = float(ajf.predict(h)); s = cf[1][ts.searchsorted(h, side='right') - 1]; k = 1 - float(km.predict(h)); mx = max(mx, abs(a - s)); viol += k < a - 1e-9
print(f"  max |lifelines - sksurv| over 40 horizons = {mx:.2e}; 1-KM<CIF violations = {viol}; at t=3: AJ {float(ajf.predict(3.0)):.4f} 1-KM {1-float(km.predict(3.0)):.4f}")
assert mx < 1e-6 and viol == 0
print("== lifelines AJ tie warning")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always"); AalenJohansenFitter(calculate_variance=False).fit(np.array([1, 1, 2, 3.]), np.array([1, 2, 1, 0]), event_of_interest=1)
print("  ties ->", [str(x.message)[:90] for x in w])
assert any("tie" in str(x.message).lower() for x in w)
print("== attribute search: Fine-Gray / CIF-Brier names in lifelines / sksurv / pycox")
import lifelines, sksurv, pkgutil, importlib
hits = []
for pkg in (lifelines, sksurv):
    for m in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        n = m.name.lower()
        if any(k in n for k in ("fine", "gray", "subdist")): hits.append(m.name)
print("  module names containing fine/gray/subdist:", hits or "none")
print("== lifelines concordance sign trap (GBSG2, held-out)")
from sksurv.datasets import load_gbsg2
from sksurv.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sksurv.metrics import concordance_index_censored
X, y = load_gbsg2(); Xn = OneHotEncoder().fit_transform(X).astype(float)
df = Xn.copy(); df["time"] = y["time"].astype(float); df["event"] = y["cens"].astype(int)
tr, te = train_test_split(df, test_size=0.3, random_state=0, stratify=df["event"])
cph = CoxPHFitter(penalizer=0.1).fit(tr, "time", "event"); ph = cph.predict_partial_hazard(te)
wrong = concordance_index(te["time"], ph, te["event"]); right = concordance_index(te["time"], -ph, te["event"])
sk = concordance_index_censored(te["event"].astype(bool), te["time"], ph.values)[0]
print(f"  lifelines concordance_index(time, partial_hazard, event) = {wrong:.4f}; with -partial_hazard = {right:.4f}; wrong+right = {wrong+right:.4f}; sksurv concordance_index_censored(risk=partial hazard) = {sk:.4f}")
assert wrong < 0.5 < right and abs(wrong + right - 1) < 1e-9 and abs(sk - right) < 1e-9
print("  PASS: SKILL.md says negate for lifelines; sksurv takes risk directly (higher = higher risk)")
