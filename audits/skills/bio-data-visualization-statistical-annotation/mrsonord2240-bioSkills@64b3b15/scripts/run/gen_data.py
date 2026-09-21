# SYNTHETIC data with planted effects. Written for the statistical-annotation audit.
import numpy as np, pandas as pd, os
D = r"F:\OpenScience\audits\bio-data-visualization-statistical-annotation\data"
rng = np.random.default_rng(20260920)

# 1. three-group skewed (lognormal), UNEQUAL n. Treatment planted effect; Vehicle = planted null vs Control
ctrl = rng.lognormal(1.0, 0.5, 12)
trt  = rng.lognormal(1.9, 0.5, 15)
veh  = rng.lognormal(1.0, 0.5, 9)
df = pd.DataFrame({"group": ["Control"]*12 + ["Treatment"]*15 + ["Vehicle"]*9,
                   "value": np.concatenate([ctrl, trt, veh])})
df.to_csv(os.path.join(D, "three_group.csv"), index=False)

# 2. four-group (6 comparisons): A ref, B null, C moderate effect, D borderline effect; unequal n
g = {"A": rng.normal(10, 2, 14), "B": rng.normal(10, 2, 11), "C": rng.normal(12.6, 2, 16), "D": rng.normal(11.6, 2, 9)}
pd.DataFrame([(k, v) for k, vs in g.items() for v in vs], columns=["group", "value"]).to_csv(os.path.join(D, "four_group.csv"), index=False)

# 3. paired: 14 subjects, large between-subject variance, consistent within-subject shift
subj = rng.normal(50, 15, 14)
pre = subj + rng.normal(0, 1.5, 14)
post = subj + 2.5 + rng.normal(0, 1.5, 14)
pd.DataFrame({"subject_id": [f"S{i+1:02d}" for i in range(14)]*2, "time": ["Pre"]*14 + ["Post"]*14,
              "value": np.concatenate([pre, post])}).to_csv(os.path.join(D, "paired.csv"), index=False)

# 4. nested: 2 groups x 4 patients x 150 cells; big patient random effect, NO true group effect
rows = []
for grp in ["Ctl", "Trt"]:
    for p in range(4):
        pe = rng.normal(0, 1.0)
        for v in rng.normal(pe, 0.5, 150):
            rows.append((grp, f"{grp}_P{p+1}", v))
pd.DataFrame(rows, columns=["group", "subject_id", "value"]).to_csv(os.path.join(D, "nested.csv"), index=False)

# 5. large N tiny effect
pd.DataFrame({"group": ["X"]*5000 + ["Y"]*5000,
              "value": np.concatenate([rng.normal(0, 1, 5000), rng.normal(0.08, 1, 5000)])}).to_csv(os.path.join(D, "bigN.csv"), index=False)
print("ok")
