"""Re-audit (2026-09-19): fresh synthetic 2-hashtag HTO dataset, independent of the
fixer's own test data (different seed, different cell count). Not real experimental data.
Used to independently verify the P0 fix for scanpy.external.pp.hashsolo at exactly 2 tags.
"""
import numpy as np
import pandas as pd
import anndata as ad

rng = np.random.default_rng(919200226)  # different seed from fixer/original auditor

n_cells = 750
tag_names = np.array(["TAG_1", "TAG_2"])
singlet_rate, doublet_rate = 0.82, 0.06
neg_rate = 1 - singlet_rate - doublet_rate
classes = rng.choice(["singlet", "doublet", "negative"], size=n_cells,
                      p=[singlet_rate, doublet_rate, neg_rate])
counts = np.zeros((n_cells, 2), dtype=int)
true_sample = []
for i, cls in enumerate(classes):
    bg = rng.poisson(9, size=2)
    counts[i] = bg
    if cls == "singlet":
        t = rng.integers(0, 2)
        counts[i, t] += rng.poisson(200)
        true_sample.append(tag_names[t])
    elif cls == "doublet":
        counts[i] += rng.poisson(170, size=2)
        true_sample.append("TAG_1+TAG_2")
    else:
        true_sample.append("Negative")

hto_cols = list(tag_names)
hto_df = pd.DataFrame(counts, columns=hto_cols,
                       index=[f"C{i:05d}" for i in range(n_cells)])
hto_df["true_class"] = classes
hto_df["true_sample"] = true_sample
hto_df.to_csv("hto_2tag_fresh.csv")
print("class counts:", pd.Series(classes).value_counts().to_dict())
