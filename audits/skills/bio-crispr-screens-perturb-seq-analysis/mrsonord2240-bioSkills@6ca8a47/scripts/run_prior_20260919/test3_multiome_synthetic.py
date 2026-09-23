"""
Re-auditor's own synthetic RNA+ATAC (multiome) fixture for the fixed
'Multiomic Perturb-seq (RNA + ATAC)' section of SKILL.md.

Independent of the fixer's fixture: different seed, different cell/gene/peak
counts, different planted-signal count and effect sizes. Follows the SKILL.md
recipe verbatim: propagate mixscape_class from RNA to ATAC via shared
obs_names, then normalize_total + log1p + rank_genes_groups(wilcoxon) on the
ATAC side (NOT TF-IDF, per the Skill's documented rationale).
"""
import numpy as np
import pandas as pd
import anndata as ad
import muon as mu
import scanpy as sc

rng = np.random.default_rng(4471)

n_cells = 620
n_genes = 90
n_peaks = 55
n_planted_genes = 6
n_planted_peaks = 6

cell_ids = [f"cell{i}" for i in range(n_cells)]
# Half KO, half NTC
group = np.array(["GENE_A KO"] * (n_cells // 2) + ["NTC"] * (n_cells - n_cells // 2))
rng.shuffle(group)

# --- RNA side ---
gene_names = [f"GENE{i:03d}" for i in range(n_genes)]
gene_baseline = rng.uniform(5, 300, size=n_genes)
gene_true_lfc = np.zeros(n_genes)
gene_true_lfc[:n_planted_genes] = rng.choice([-1, 1], size=n_planted_genes) * rng.uniform(1.5, 3.0, size=n_planted_genes)

rna_counts = np.zeros((n_cells, n_genes))
for i in range(n_cells):
    mult = np.where(group[i] == "GENE_A KO", 2 ** gene_true_lfc, 1.0)
    mean = gene_baseline * mult
    rna_counts[i, :] = rng.poisson(mean)

adata_rna = ad.AnnData(
    X=rna_counts,
    obs=pd.DataFrame({"mixscape_class": group}, index=cell_ids),
    var=pd.DataFrame(index=gene_names),
)

# --- ATAC side (separate count matrix, shared obs_names/cells) ---
peak_names = [f"PEAK{i:03d}" for i in range(n_peaks)]
peak_baseline = rng.uniform(2, 80, size=n_peaks)
peak_true_lfc = np.zeros(n_peaks)
peak_true_lfc[:n_planted_peaks] = rng.choice([-1, 1], size=n_planted_peaks) * rng.uniform(1.5, 3.0, size=n_planted_peaks)

atac_counts = np.zeros((n_cells, n_peaks))
for i in range(n_cells):
    mult = np.where(group[i] == "GENE_A KO", 2 ** peak_true_lfc, 1.0)
    mean = peak_baseline * mult
    atac_counts[i, :] = rng.poisson(mean)

adata_atac = ad.AnnData(
    X=atac_counts,
    obs=pd.DataFrame(index=cell_ids),  # deliberately WITHOUT mixscape_class -- must be propagated
    var=pd.DataFrame(index=peak_names),
)

print(f"RNA: {adata_rna.n_obs} cells x {adata_rna.n_vars} genes")
print(f"ATAC: {adata_atac.n_obs} cells x {adata_atac.n_vars} peaks")
print(f"Planted DE genes: {gene_names[:n_planted_genes]} (true log2FC: {gene_true_lfc[:n_planted_genes].round(2)})")
print(f"Planted DA peaks: {peak_names[:n_planted_peaks]} (true log2FC: {peak_true_lfc[:n_planted_peaks].round(2)})")

# --- Follow SKILL.md recipe ---
mdata = mu.MuData({"rna": adata_rna, "atac": adata_atac})

assert "mixscape_class" not in mdata["atac"].obs.columns, "test setup error: atac already has mixscape_class"
mdata["atac"].obs["mixscape_class"] = mdata["rna"].obs["mixscape_class"]
assert "mixscape_class" in mdata["atac"].obs.columns
print("\nCONFIRMED: mixscape_class propagated from RNA to ATAC modality via shared obs_names.")

atac_pert = mdata["atac"][mdata["atac"].obs["mixscape_class"].isin(["GENE_A KO", "NTC"])].copy()
sc.pp.normalize_total(atac_pert)
sc.pp.log1p(atac_pert)
sc.tl.rank_genes_groups(atac_pert, groupby="mixscape_class", groups=["GENE_A KO"], reference="NTC", method="wilcoxon")
peak_result = sc.get.rank_genes_groups_df(atac_pert, group="GENE_A KO")

print("\n--- ATAC differential peaks (top 10 by adjusted p-value) ---")
peak_result_sorted = peak_result.sort_values("pvals_adj")
print(peak_result_sorted.head(10)[["names", "logfoldchanges", "pvals_adj"]])

planted_peak_set = set(peak_names[:n_planted_peaks])
top10_peaks = set(peak_result_sorted.head(10)["names"])
recovered_peaks = planted_peak_set & top10_peaks
print(f"\nPlanted peaks recovered in top 10: {len(recovered_peaks)}/{n_planted_peaks} -> {sorted(recovered_peaks)}")

# --- RNA-side DE for comparison (plain scanpy rank_genes_groups on RNA counts, since
#     PyDESeq2 is already independently verified in test1/test2 -- here we just need
#     to confirm the "recovers planted structure" claim end to end on the RNA arm too) ---
adata_rna_norm = adata_rna.copy()
sc.pp.normalize_total(adata_rna_norm)
sc.pp.log1p(adata_rna_norm)
sc.tl.rank_genes_groups(adata_rna_norm, groupby="mixscape_class", groups=["GENE_A KO"], reference="NTC", method="wilcoxon")
gene_result = sc.get.rank_genes_groups_df(adata_rna_norm, group="GENE_A KO")
gene_result_sorted = gene_result.sort_values("pvals_adj")
print("\n--- RNA differential genes (top 10 by adjusted p-value) ---")
print(gene_result_sorted.head(10)[["names", "logfoldchanges", "pvals_adj"]])

planted_gene_set = set(gene_names[:n_planted_genes])
top10_genes = set(gene_result_sorted.head(10)["names"])
recovered_genes = planted_gene_set & top10_genes
print(f"\nPlanted genes recovered in top 10: {len(recovered_genes)}/{n_planted_genes} -> {sorted(recovered_genes)}")

assert len(recovered_peaks) >= 5, f"Expected most planted peaks recovered, got {len(recovered_peaks)}/{n_planted_peaks}"
assert len(recovered_genes) >= 5, f"Expected most planted genes recovered, got {len(recovered_genes)}/{n_planted_genes}"

print("\nPASS: multiome workflow (mixscape_class propagation + normalize_total+log1p + wilcoxon) "
      "recovers planted DE/DA structure on an independently-seeded synthetic RNA+ATAC dataset.")
