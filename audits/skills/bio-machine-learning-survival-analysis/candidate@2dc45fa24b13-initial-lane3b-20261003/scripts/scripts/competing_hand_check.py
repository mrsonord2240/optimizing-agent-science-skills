"""1-KM vs Aalen-Johansen CIF against hand-computed values on a tiny table, plus lifelines behavior with tied times.
Table (time, cause; 0 = censored): (1,1) (2,2) (3,1) (4,0) (5,2) (6,1)"""
import warnings
import numpy as np
from lifelines import KaplanMeierFitter, AalenJohansenFitter
T = np.array([1, 2, 3, 4, 5, 6.]); C = np.array([1, 2, 1, 0, 2, 1])
# Hand computation. CIF1(t) = sum over event times <= t of S(t-) * d1 / n, S = all-cause KM.
S = 1.0; cif = 0.0; n = 6; hand_cif = {}
for t, c in zip(T, C):
    if c == 1:
        cif += S * (1 / n)
    if c in (1, 2):
        S *= (1 - 1 / n)
    n -= 1; hand_cif[t] = cif
# 1-KM with cause 2 treated as censoring
S1 = 1.0; n = 6; km_hand = {}
for t, c in zip(T, C):
    if c == 1:
        S1 *= (1 - 1 / n)
    n -= 1; km_hand[t] = 1 - S1
ajf = AalenJohansenFitter(calculate_variance=False).fit(T, C, event_of_interest=1)
km = KaplanMeierFitter().fit(T, event_observed=(C == 1))
print(f"{'t':>3} {'hand CIF1':>10} {'lifelines AJ':>13} {'hand 1-KM':>10} {'lifelines 1-KM':>15}")
for t in T:
    a = float(ajf.predict(t)); k = 1 - float(km.predict(t))
    print(f"{t:3.0f} {hand_cif[t]:10.4f} {a:13.4f} {km_hand[t]:10.4f} {k:15.4f}")
    assert abs(a - hand_cif[t]) < 1e-6 and abs(k - km_hand[t]) < 1e-6
print("hand values match lifelines; 1-KM >= CIF at every t:", all(km_hand[t] >= hand_cif[t] - 1e-12 for t in T))
# Ties: the Skill's demo uses continuous times; real data has ties. lifelines AJ jitters tied times.
T2 = np.array([1, 1, 2, 3, 3, 4, 5, 6.]); C2 = np.array([1, 2, 1, 2, 1, 0, 2, 1])
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    runs = [float(AalenJohansenFitter(calculate_variance=False, seed=s).fit(T2, C2, event_of_interest=1).predict(6.0)) for s in (0, 1, 2)]
print("AJ CIF1(6) on tied data across jitter seeds:", [round(r, 4) for r in runs], "warnings:", sorted({str(x.message)[:100] for x in w}))
