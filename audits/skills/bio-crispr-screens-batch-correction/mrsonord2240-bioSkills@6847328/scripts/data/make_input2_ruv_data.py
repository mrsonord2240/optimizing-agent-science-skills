"""Build a small synthetic dataset for Input 2 (RUV, unknown/unannotated batch).
Realistic pooled-screen shape: 2000 targeting guides (500 genes x 4 guides) + 500
non-targeting controls, 8 samples split across 2 UNANNOTATED batches (the whole
point of RUV is the analyst does NOT know which samples are in which batch --
only that NTCs should be flat)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
n_genes = 500
guides_per_gene = 4
n_guides = n_genes * guides_per_gene
n_ntc = 500

gene_names = [f"Gene_{i:04d}" for i in range(n_genes)]
genes = np.repeat(gene_names, guides_per_gene)
guide_ids = [f"{g}_g{i+1}" for g in gene_names for i in range(guides_per_gene)]

samples = [f"S{i+1}" for i in range(8)]
# TRUE (unannotated-to-the-analyst) batch membership: first 4 samples deeper sequencing,
# last 4 shallower + a mild additive background -- unknown technical batch, not disclosed to RUV.
true_batch = ["deep"] * 4 + ["shallow"] * 4
condition = ["ctrl", "ctrl", "treat", "treat"] * 2

base = 800
counts = {}
essential = gene_names[:30]
for j, s in enumerate(samples):
    depth_factor = 1.0 if true_batch[j] == "deep" else 0.55
    add = 0 if true_batch[j] == "deep" else 80
    lam = np.full(n_guides, base * depth_factor + add)
    if condition[j] == "treat":
        is_ess = np.isin(genes, essential)
        lam[is_ess] *= 0.25  # essential dropout under treat
    counts[s] = rng.poisson(lam).astype(float)

df = pd.DataFrame({"gene": genes, "guide": guide_ids, **counts})

ntc_rows = []
for i in range(n_ntc):
    row = {"gene": f"NonTargeting_{i+1:03d}", "guide": f"NT_{i+1:03d}"}
    for j, s in enumerate(samples):
        depth_factor = 1.0 if true_batch[j] == "deep" else 0.55
        add = 0 if true_batch[j] == "deep" else 80
        row[s] = rng.poisson(base * depth_factor + add)
    ntc_rows.append(row)
df = pd.concat([df, pd.DataFrame(ntc_rows)], ignore_index=True)

df.to_csv(r"F:\OpenScience\audits\bio-crispr-screens-batch-correction\data\input2_ruv_counts.csv", index=False)
meta = pd.DataFrame({"sample": samples, "true_batch_HIDDEN": true_batch, "condition": condition})
meta.to_csv(r"F:\OpenScience\audits\bio-crispr-screens-batch-correction\data\input2_ruv_TRUE_batch_ground_truth.csv", index=False)
print("Wrote", df.shape, "guides x samples (incl. gene/guide id cols)")
print("Essential genes (should drop under treat):", essential[:5], "...")
