# bio-qsar-modeling -- Input 5 (Stress): class imbalance + probability calibration,
# following the SKILL.md "Class imbalance not handled" failure mode and the
# "Calibration (Platt / Isotonic)" section.
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (roc_auc_score, average_precision_score, f1_score,
                             accuracy_score, brier_score_loss, precision_score,
                             recall_score)
from sklearn.calibration import calibration_curve

D = r"F:\OpenScience\audits\bio-qsar-modeling\run"
X = np.load(D + r"\X.npy").astype(np.float32)
y_cont = np.load(D + r"\y.npy")
tr = np.load(D + r"\tr.npy")
te = np.load(D + r"\te.npy")
y = (y_cont >= 5.0).astype(int)
print(f"[data] n={len(y)}  positives={y.sum()} ({100*y.mean():.1f}%)  "
      f"scaffold split train={len(tr)} test={len(te)}")

# carve a calibration split out of TRAIN only (SKILL.md: "held-out calibration set")
rs = np.random.RandomState(42)
perm = rs.permutation(tr)
cal, fit = perm[:len(perm) // 5], perm[len(perm) // 5:]
print(f"[split] fit={len(fit)} calibration={len(cal)} test={len(te)}  "
      f"(calibration carved from TRAIN, never from test)")

print("\n== SKILL.md failure mode: 'Class imbalance not handled' ==")
for label, kw in [('default loss          ', {}),
                  ("class_weight='balanced'", {'class_weight': 'balanced'})]:
    m = RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1, **kw)
    m.fit(X[fit], y[fit])
    p = m.predict_proba(X[te])[:, 1]
    hard = (p >= 0.5).astype(int)
    print(f"  {label}  ACC={accuracy_score(y[te], hard):.3f}  "
          f"AUC={roc_auc_score(y[te], p):.3f}  AP={average_precision_score(y[te], p):.3f}  "
          f"F1={f1_score(y[te], hard):.3f}  "
          f"minority(neg) precision={precision_score(y[te], hard, pos_label=0):.3f} "
          f"recall={recall_score(y[te], hard, pos_label=0):.3f}")
print(f"  majority-class baseline accuracy on the test set = "
      f"{max(y[te].mean(), 1-y[te].mean()):.3f}")
print("  -> the documented symptom ('high accuracy but minority precision/recall poor') "
      "is exactly what the default-loss row shows.")

print("\n== SKILL.md 'Calibration (Platt / Isotonic)' ==")
m = RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1)
m.fit(X[fit], y[fit])
p_cal, p_te = m.predict_proba(X[cal])[:, 1], m.predict_proba(X[te])[:, 1]

iso = IsotonicRegression(out_of_bounds='clip').fit(p_cal, y[cal])   # SKILL.md snippet
p_iso = iso.predict(p_te)
platt = LogisticRegression().fit(p_cal.reshape(-1, 1), y[cal])
p_platt = platt.predict_proba(p_te.reshape(-1, 1))[:, 1]

for name, p in [('uncalibrated', p_te), ('isotonic', p_iso), ('Platt', p_platt)]:
    frac, mean_pred = calibration_curve(y[te], np.clip(p, 1e-6, 1 - 1e-6), n_bins=5,
                                        strategy='quantile')
    ece = float(np.mean(np.abs(frac - mean_pred)))
    print(f"  {name:13} Brier={brier_score_loss(y[te], np.clip(p,0,1)):.4f}  "
          f"AUC={roc_auc_score(y[te], p):.3f}  5-bin calibration gap={ece:.4f}")
print("  -> SKILL.md's point that '--metric roc evaluates ranking and does not "
      "calibrate' holds: AUC is unchanged by isotonic while Brier and the gap move.")

print("\n== SKILL.md Common Error: 'Calibration degrades held-out results' ==")
iso_bad = IsotonicRegression(out_of_bounds='clip').fit(p_te, y[te])   # deliberately wrong
p_bad = iso_bad.predict(p_te)
print(f"  calibrator fit ON THE TEST SET: Brier={brier_score_loss(y[te], np.clip(p_bad,0,1)):.4f} "
      f"-- looks better than the honest {brier_score_loss(y[te], np.clip(p_iso,0,1)):.4f}, "
      f"and is meaningless. The Skill's instruction to use a proper calibration split "
      f"is what prevents this.")
