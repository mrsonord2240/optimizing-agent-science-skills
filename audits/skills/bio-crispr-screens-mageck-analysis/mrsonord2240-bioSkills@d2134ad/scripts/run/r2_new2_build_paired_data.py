import numpy as np
import pandas as pd

# Build a paired-sample design: 6 donors, each with baseline + treated sample (matched pairs)
rng = np.random.default_rng(303)
n_genes = 40
n_hits = 10
sgrna_per_gene = 4
n_donors = 6
gene_names = [f"GENE{i}" for i in range(n_genes)]
hits = set(gene_names[:n_hits])
base_mean = 400
rows = []
# donor-specific efficiency multiplier (batch/donor effect that pairing should cancel)
donor_effect = {d: rng.uniform(0.6, 1.6) for d in range(n_donors)}
for g in gene_names:
    true_mult = 0.3 if g in hits else 1.0
    for s in range(sgrna_per_gene):
        sgid = f"{g}_sg{s}"
        guide_mean = base_mean * rng.uniform(0.7, 1.3)
        row = [sgid, g]
        for d in range(n_donors):
            baseline_count = rng.poisson(guide_mean * donor_effect[d])
            treated_count = rng.poisson(max(guide_mean * donor_effect[d] * true_mult, 1))
            row += [baseline_count, treated_count]
        rows.append(row)
cols = ["sgRNA", "Gene"]
for d in range(n_donors):
    cols += [f"D{d}_baseline", f"D{d}_treat"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv("r2_new2_paired_counts.txt", sep="\t", index=False)
df.to_csv("r2_new2_paired_counts_mageck.txt", sep="\t", index=False)
print(df.shape, "hits:", sorted(hits))
