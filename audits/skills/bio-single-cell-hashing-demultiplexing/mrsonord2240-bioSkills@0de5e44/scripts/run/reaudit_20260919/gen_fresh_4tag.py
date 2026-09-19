"""Re-audit: fresh synthetic 4-tag HTO CSV for the GMM-Demux end-to-end test, independent
of the fixer's/original auditor's data.csv (different seed, different cell count).
Not real experimental data.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(31337)
n_cells = 1000
tags = ["G_A", "G_B", "G_C", "G_D"]
n_tags = len(tags)
singlet_rate, doublet_rate = 0.83, 0.07
neg_rate = 1 - singlet_rate - doublet_rate
classes = rng.choice(["singlet", "doublet", "negative"], size=n_cells,
                      p=[singlet_rate, doublet_rate, neg_rate])
counts = np.zeros((n_cells, n_tags), dtype=float)
true_sample = []
for i, cls in enumerate(classes):
    bg = rng.poisson(8, size=n_tags).astype(float)
    counts[i] = bg
    if cls == "singlet":
        t = rng.integers(0, n_tags)
        counts[i, t] += rng.poisson(230)
        true_sample.append(tags[t])
    elif cls == "doublet":
        two = rng.choice(n_tags, size=2, replace=False)
        for t in two:
            counts[i, t] += rng.poisson(200)
        true_sample.append("+".join(sorted(tags[t] for t in two)))
    else:
        true_sample.append("Negative")

df = pd.DataFrame(counts, columns=tags, index=[f"BC{i:05d}" for i in range(n_cells)])
df["true_class"] = classes
df["true_sample"] = true_sample
df.to_csv("hto_4tag_fresh.csv")
print("class counts:", pd.Series(classes).value_counts().to_dict())
