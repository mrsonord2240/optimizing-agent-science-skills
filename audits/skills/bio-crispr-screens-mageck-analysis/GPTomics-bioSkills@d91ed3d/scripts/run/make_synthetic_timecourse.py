import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n_dep, n_enr, n_neu = 10, 10, 30
sgrna_per_gene = 4
genes = ([f"DEP{i}" for i in range(n_dep)]
         + [f"ENR{i}" for i in range(n_enr)]
         + [f"NEU{i}" for i in range(n_neu)])

rows = []
base_mean = 500
for g in genes:
    if g.startswith("DEP"):
        # progressive depletion: day0=1x, day7=0.6x, day14=0.35x, day21=0.15x
        mults = [1.0, 0.6, 0.35, 0.15]
    elif g.startswith("ENR"):
        mults = [1.0, 1.6, 2.4, 3.5]
    else:
        mults = [1.0, 1.0, 1.0, 1.0]
    for s in range(sgrna_per_gene):
        sgid = f"{g}_sg{s}"
        guide_mean = base_mean * rng.uniform(0.7, 1.3)
        counts = []
        for r in range(2):  # 2 replicates per timepoint
            for m in mults:
                lam = max(guide_mean * m * rng.uniform(0.85, 1.15), 1)
                counts.append(rng.poisson(lam))
        rows.append([sgid, g] + counts)

cols = ["sgRNA", "Gene"]
samples = []
for tp in ["Day0", "Day7", "Day14", "Day21"]:
    for r in ["r1", "r2"]:
        samples.append(f"{tp}_{r}")
# reorder columns to match generation loop (rep-major: r1 all tps, r2 all tps)
gen_order = []
for r in range(2):
    for tp in ["Day0", "Day7", "Day14", "Day21"]:
        gen_order.append(f"{tp}_r{r+1}")
cols += gen_order

df = pd.DataFrame(rows, columns=cols)
# reorder to canonical sample order
df = df[["sgRNA", "Gene"] + samples]
df.to_csv("synthetic_timecourse_counts.txt", sep="\t", index=False)
print(df.head())
print(df.shape)
