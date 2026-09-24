import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

n_genes = 200
sgrna_per_gene = 4
n_ntc = 40

frac_changing = 0.45
n_changing = int(n_genes * frac_changing)
gene_names = [f"GENE{i}" for i in range(n_genes)]
rng.shuffle(gene_names)
changing = set(gene_names[:n_changing])

rows = []
gt = {}
base_mean = 500
for g in gene_names:
    if g in changing:
        mult_t18 = rng.choice([0.2, 3.0])
        gt[g] = "depleted" if mult_t18 == 0.2 else "enriched"
    else:
        mult_t18 = 1.0
        gt[g] = "neutral"
    for s in range(sgrna_per_gene):
        sgid = f"{g}_sg{s}"
        guide_mean = base_mean * rng.uniform(0.7, 1.3)
        t0 = rng.poisson(guide_mean)
        reps = [rng.poisson(max(guide_mean * mult_t18 * rng.uniform(0.85, 1.15), 1)) for _ in range(3)]
        rows.append([sgid, g, t0] + reps)

ntc_ids = []
for i in range(n_ntc):
    sgid = f"NTC_{i:04d}"
    g = "NonTargeting"
    guide_mean = base_mean * rng.uniform(0.7, 1.3)
    t0 = rng.poisson(guide_mean)
    reps = [rng.poisson(max(guide_mean * rng.uniform(0.85, 1.15), 1)) for _ in range(3)]
    rows.append([sgid, g, t0] + reps)
    ntc_ids.append(sgid)

cols = ["sgRNA", "Gene", "T0", "T18_r1", "T18_r2", "T18_r3"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv("r2_regen_heavy_selection_counts.txt", sep="\t", index=False)

gtdf = pd.DataFrame(list(gt.items()), columns=["Gene", "truth"])
gtdf.to_csv("r2_heavy_selection_ground_truth.txt", sep="\t", index=False)
print("depleted:", sum(v == 'depleted' for v in gt.values()),
      "enriched:", sum(v == 'enriched' for v in gt.values()),
      "neutral:", sum(v == 'neutral' for v in gt.values()))
