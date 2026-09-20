"""Synthetic Perturb-seq dataset for auditing bio-crispr-screens-perturb-seq-analysis.
NOT real biological data -- fabricated for testing the Skill's code patterns only.
"""
import numpy as np
import anndata as ad
import pandas as pd

rng = np.random.default_rng(42)

n_cells = 2000
n_genes = 300
perts = ["NTC", "GENE_A", "GENE_B", "GENE_C", "GENE_D"]
# NTC gets 30%, others split the remaining 70%
probs = [0.30] + [0.70 / 4] * 4
pert_assignment = rng.choice(perts, size=n_cells, p=probs)

# Baseline negative-binomial-ish counts (use NB via gamma-Poisson mixture)
gene_means = rng.gamma(shape=2.0, scale=5.0, size=n_genes)
counts = rng.poisson(gene_means[None, :] * rng.gamma(2.0, 0.5, size=(n_cells, 1)))

# GENE_A is a "real" perturbation: depress a responder gene module (genes 0-19) ~3x
responder_genes = slice(0, 20)
is_gene_a = pert_assignment == "GENE_A"
counts[is_gene_a, responder_genes] = rng.poisson(
    gene_means[responder_genes][None, :] * 0.33 * rng.gamma(2.0, 0.5, size=(is_gene_a.sum(), 1))
)
# GENE_B is a "weak/no effect" perturbation (indistinguishable from NTC) -- to exercise the
# Mixscape "escaper" / weak-phenotype failure mode described in the Skill's Failure Modes section.

adata = ad.AnnData(
    X=counts.astype(np.float32),
    obs=pd.DataFrame({"perturbation": pert_assignment}, index=[f"cell{i}" for i in range(n_cells)]),
    var=pd.DataFrame(index=[f"gene{i}" for i in range(n_genes)]),
)
adata.obs["perturbation"] = adata.obs["perturbation"].astype("category")
adata.obs["n_umi"] = adata.X.sum(axis=1)
adata.obs["n_genes"] = (adata.X > 0).sum(axis=1)
adata.obs["channel"] = rng.choice(["chan1", "chan2"], size=n_cells)

adata.write_h5ad("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/synthetic_perturbseq.h5ad")
print(f"Wrote synthetic AnnData: {adata.n_obs} cells x {adata.n_vars} genes")
print(adata.obs["perturbation"].value_counts())

# --- Separate synthetic sgRNA-counts matrix for the sgRNA-assignment function test ---
n_cells2 = 500
sgrnas = ["sg_NTC1", "sg_NTC2", "sg_GENE_A_1", "sg_GENE_A_2", "sg_GENE_B_1"]
sg_counts = rng.poisson(0.5, size=(n_cells2, len(sgrnas)))
# Force ~70% of cells to have exactly one sgRNA at high count (>=10 reads)
n_single = int(n_cells2 * 0.70)
single_idx = rng.choice(n_cells2, size=n_single, replace=False)
single_sg = rng.integers(0, len(sgrnas), size=n_single)
for i, sg in zip(single_idx, single_sg):
    sg_counts[i, sg] = rng.integers(15, 200)
# Force ~5% multiplets (two sgRNAs both >=10 reads)
remaining = np.setdiff1d(np.arange(n_cells2), single_idx)
n_multi = int(n_cells2 * 0.05)
multi_idx = rng.choice(remaining, size=n_multi, replace=False)
for i in multi_idx:
    two = rng.choice(len(sgrnas), size=2, replace=False)
    sg_counts[i, two] = rng.integers(15, 200, size=2)

sg_adata = ad.AnnData(
    X=np.zeros((n_cells2, len(sgrnas)), dtype=np.float32),
    obs=pd.DataFrame(index=[f"cell{i}" for i in range(n_cells2)]),
    var=pd.DataFrame(index=sgrnas),
)
sg_adata.layers["sgrna_counts"] = sg_counts.astype(np.float32)
sg_adata.write_h5ad("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/synthetic_sgrna.h5ad")
np.save("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/sgrna_counts.npy", sg_counts)
with open("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/sgrna_names.txt", "w") as f:
    f.write("\n".join(sgrnas))
print(f"Wrote synthetic sgRNA counts matrix: {sg_counts.shape}")
