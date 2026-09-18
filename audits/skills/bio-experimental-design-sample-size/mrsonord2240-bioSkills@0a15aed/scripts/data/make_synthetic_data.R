# Synthetic data for the re-audit of bio-experimental-design-sample-size.
# Fresh seed (20260918 + 7), generated independently of the pre-fix audit's and the
# fixer's own synthetic data/scripts (different RNG stream, different planted values
# where it doesn't matter, same order of magnitude where realism requires it).
set.seed(20260925)
suppressPackageStartupMessages(library(DESeq2))

out_dir <- "data"

# ---------------------------------------------------------------------------
# 1. Bulk RNA-seq 2v2 and 6v6 pilots, NB-distributed, planted dispersion 0.30
# ---------------------------------------------------------------------------
simulate_pilot <- function(n_per_group, ngenes = 8000, planted_disp = 0.30, base_mean = 220) {
  mu_gene <- rlnorm(ngenes, meanlog = log(base_mean), sdlog = 0.9)
  cond <- factor(rep(c("A", "B"), each = n_per_group))
  counts <- matrix(0L, nrow = ngenes, ncol = 2 * n_per_group)
  for (g in seq_len(ngenes)) {
    size <- 1 / planted_disp
    counts[g, ] <- rnbinom(2 * n_per_group, mu = mu_gene[g], size = size)
  }
  rownames(counts) <- paste0("gene", seq_len(ngenes))
  colnames(counts) <- paste0("s", seq_len(2 * n_per_group))
  coldata <- data.frame(condition = cond, row.names = colnames(counts))
  list(counts = counts, coldata = coldata)
}

pilot_2v2 <- simulate_pilot(2)
pilot_6v6 <- simulate_pilot(6)

write.csv(pilot_2v2$counts, file.path(out_dir, "pilot_2v2_counts.csv"))
write.csv(pilot_2v2$coldata, file.path(out_dir, "pilot_2v2_coldata.csv"))
write.csv(pilot_6v6$counts, file.path(out_dir, "pilot_6v6_counts.csv"))
write.csv(pilot_6v6$coldata, file.path(out_dir, "pilot_6v6_coldata.csv"))

# ---------------------------------------------------------------------------
# 2. scRNA-seq donor-level pilot: 8 donors (4 vs 4), 120 cells/donor, 3000 genes
#    Planted donor-level dispersion ~0.40, condition effect on 5% of genes (lfc=1.5)
# ---------------------------------------------------------------------------
ngenes_sc <- 3000
n_donors <- 8
cells_per_donor <- 120
donor_condition <- rep(c("disease", "control"), each = n_donors / 2)
p_de <- 0.05
true_lfc <- log2(1.6)
de_genes <- sample(seq_len(ngenes_sc), size = round(ngenes_sc * p_de))

gene_base <- rlnorm(ngenes_sc, meanlog = log(3), sdlog = 1.0)  # per-cell mean counts
donor_disp <- 0.40

cell_counts <- list()
for (d in seq_len(n_donors)) {
  is_disease <- donor_condition[d] == "disease"
  mu_d <- gene_base
  if (is_disease) mu_d[de_genes] <- mu_d[de_genes] * 2^true_lfc
  mat <- matrix(0L, nrow = ngenes_sc, ncol = cells_per_donor)
  for (g in seq_len(ngenes_sc)) {
    mat[g, ] <- rnbinom(cells_per_donor, mu = mu_d[g], size = 1 / donor_disp)
  }
  rownames(mat) <- paste0("gene", seq_len(ngenes_sc))
  colnames(mat) <- paste0("donor", d, "_cell", seq_len(cells_per_donor))
  cell_counts[[paste0("donor", d)]] <- mat
}
saveRDS(cell_counts, file.path(out_dir, "scrna_donor_cellcounts.rds"))
write.csv(data.frame(donor = paste0("donor", seq_len(n_donors)), condition = donor_condition),
          file.path(out_dir, "scrna_donor_condition.csv"), row.names = FALSE)
writeLines(as.character(de_genes), file.path(out_dir, "scrna_true_de_genes.txt"))

# ---------------------------------------------------------------------------
# 3. Proteomics panels: m=5000 (discovery-wide) and m=50 (targeted hypothesis panel)
#    10% truly changed at Cohen's d = 1.2, 20% MNAR dropout, for BH-power simulation.
# ---------------------------------------------------------------------------
make_proteomics_panel <- function(m, p_changed = 0.10, d_true = 1.2, seed_offset = 0) {
  set.seed(20260925 + seed_offset)
  changed <- sample(seq_len(m), size = round(m * p_changed))
  list(m = m, changed = changed, d_true = d_true)
}
panel_5000 <- make_proteomics_panel(5000, seed_offset = 1)
panel_50   <- make_proteomics_panel(50, seed_offset = 2)
saveRDS(panel_5000, file.path(out_dir, "proteomics_panel_5000.rds"))
saveRDS(panel_50, file.path(out_dir, "proteomics_panel_50.rds"))

cat("Synthetic data generation complete.\n")
cat("Pilots: 2v2 (planted disp 0.30), 6v6 (planted disp 0.30), ngenes=8000, base_mean~220 (lognormal)\n")
cat("scRNA: 8 donors (4v4), 120 cells/donor, ngenes=3000, donor disp 0.40, true lfc=1.6 on 5% genes\n")
cat("Proteomics panels: m=5000 (10% changed, d=1.2), m=50 (10% changed, d=1.2)\n")
