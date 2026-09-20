# Synthetic in-vivo CRISPR screen count data.
# Simulates a focused library (per SKILL.md guidance: 500-3000 genes, 4 sgRNAs/gene)
# scaled down for a fast audit run: 60 genes x 4 sgRNAs = 240 sgRNAs, plasmid + 6 "animals".
# 5 genes are planted as true depleted hits (tumor suppressors / essential-in-vivo genes);
# the rest are noise, to check whether MAGeCK + the Skill's per-animal meta-analysis
# recovers the planted hits despite simulated inter-animal (bottleneck) variability.
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260919)

n_genes = 60
sgrnas_per_gene = 4
genes = [f"Gene{i:03d}" for i in range(n_genes)]
true_hits = genes[:5]  # Gene000..Gene004 planted as depleted in vivo

rows = []
for g in genes:
    for s in range(sgrnas_per_gene):
        rows.append({"sgRNA": f"{g}_sg{s}", "gene": g})
lib = pd.DataFrame(rows)
n_sg = len(lib)

plasmid_mean = 500
plasmid_counts = rng.negative_binomial(n=20, p=20 / (20 + plasmid_mean), size=n_sg)
plasmid_counts = np.clip(plasmid_counts, 20, None)

n_animals = 6
animal_cols = {}
for a in range(1, n_animals + 1):
    # Bottleneck: each animal keeps a different random ~70% of sgRNAs at near-normal
    # abundance and drops the rest sharply (clonal bottleneck simulation).
    keep_frac = rng.uniform(0.55, 0.85)
    survive = rng.random(n_sg) < keep_frac
    base = plasmid_counts.astype(float).copy()
    # depletion for true hits (stronger, but noisy across animals -- inter-animal variability)
    hit_mask = lib["gene"].isin(true_hits).values
    depletion = rng.uniform(0.05, 0.35, size=n_sg)  # residual fraction remaining
    counts = base.copy()
    counts[hit_mask] = base[hit_mask] * depletion[hit_mask]
    # bottleneck collapse for non-surviving guides
    counts[~survive] = counts[~survive] * rng.uniform(0.01, 0.1, size=(~survive).sum())
    # general in vivo noise (overdispersion)
    counts = rng.negative_binomial(
        n=8, p=8 / (8 + np.clip(counts, 1, None))
    )
    animal_cols[f"Animal{a}"] = counts

out = lib.copy()
out["Plasmid"] = plasmid_counts
for k, v in animal_cols.items():
    out[k] = v

out_path = "in_vivo_counts.txt"
out.to_csv(out_path, sep="\t", index=False)
print("Wrote", out_path, out.shape)
print("Planted true hits:", true_hits)
print(out.head())
