import numpy as np
import pandas as pd

rng = np.random.default_rng(55)

n_hit, n_neutral = 15, 45
base_mean = 500

cell_lines = ["A", "B"]
batches = ["1", "2"]
conditions = ["baseline", "treat"]

samples = []
sample_meta = []
for cl in cell_lines:
    for b in batches:
        for cond in conditions:
            for r in [1, 2]:
                sid = f"{cl}_{b}_{cond}_r{r}"
                samples.append(sid)
                sample_meta.append((cl, b, cond))

genes = [f"HIT{i}" for i in range(n_hit)] + [f"NEU{i}" for i in range(n_neutral)]
rows = []
for g in genes:
    is_hit = g.startswith("HIT")
    for s in range(4):
        sgid = f"{g}_sg{s}"
        guide_mean = base_mean * rng.uniform(0.8, 1.2)
        # cell-line effect: line B has slightly lower baseline representation (batch/cell-line variance)
        vals = []
        for (cl, b, cond) in sample_meta:
            cl_factor = 1.0 if cl == "A" else 0.8
            batch_factor = 1.0 if b == "1" else 1.15
            treat_mult = 1.0
            if cond == "treat" and is_hit:
                treat_mult = 0.3  # true depletion under treatment, consistent across lines/batches
            lam = max(guide_mean * cl_factor * batch_factor * treat_mult * rng.uniform(0.9, 1.1), 1)
            vals.append(rng.poisson(lam))
        rows.append([sgid, g] + vals)

df = pd.DataFrame(rows, columns=["sgRNA", "Gene"] + samples)
df.to_csv("synthetic_multiline_counts.txt", sep="\t", index=False)

# Design matrix: baseline, cellline_B, batch_2, treatment
design_rows = []
for sid, (cl, b, cond) in zip(samples, sample_meta):
    cellline_B = 1 if cl == "B" else 0
    batch_2 = 1 if b == "2" else 0
    treatment = 1 if cond == "treat" else 0
    design_rows.append([sid, 1, cellline_B, batch_2, treatment])
design = pd.DataFrame(design_rows, columns=["Samples", "baseline", "cellline_B", "batch_2", "treatment"])
design.to_csv("design_multiline.txt", sep="\t", index=False)
print(df.shape, "samples:", len(samples))
print(design)
