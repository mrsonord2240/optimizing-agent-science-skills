# Input 4 (Variant B) — regression of pre-fix Input 4.
# Prompt: "I'm planning an scRNA-seq disease-vs-control study. I have a small 8-donor
# pilot (4v4, 120 cells/donor). How many donors do I need for the full study?"
# Pre-fix: this route had ZERO executable code anywhere (P1 finding). Post-fix SKILL.md
# adds a full pseudobulk-on-donors block. This is the first time it has ever been run.
suppressPackageStartupMessages({
  library(DESeq2)
  library(ssizeRNA)
})

cell_counts <- readRDS("data/scrna_donor_cellcounts.rds")
donor_meta <- read.csv("data/scrna_donor_condition.csv")
donor_condition <- donor_meta$condition
true_de_genes <- as.integer(readLines("data/scrna_true_de_genes.txt"))

cat("=== SKILL.md's pseudobulk-on-donors block, run verbatim on the pattern ===\n")
set.seed(20260918)
pseudobulk <- sapply(cell_counts, rowSums)  # genes x donors
cat("Pseudobulk matrix dim:", dim(pseudobulk), "\n")
coldata <- data.frame(condition = donor_condition)
rownames(coldata) <- colnames(pseudobulk)

dds <- DESeqDataSetFromMatrix(pseudobulk, coldata, ~ condition)
dds <- DESeq(dds)
disp_vec <- dispersions(dds)
mu_vec <- rowMeans(counts(dds, normalized = TRUE))
keep <- is.finite(disp_vec) & is.finite(mu_vec) & mu_vec > 0
disp_vec <- disp_vec[keep]; mu_vec <- mu_vec[keep]
cat(sprintf("Recovered pseudobulk dispersion: median=%.3f, mean=%.3f (planted per-cell disp was 0.40 -- pseudobulk\n",
            median(disp_vec), mean(disp_vec)))
cat("dispersion is expected to differ from the per-cell value since it summarizes across summed cells)\n")

set.seed(20260918)
res <- ssizeRNA_vary(nGenes = length(mu_vec), pi0 = 0.95, mu = mu_vec, disp = disp_vec,
                     fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)
n_donors <- res$ssize[, "ssize"]
cat(sprintf("Donor sizing result: n=%s donors/group, is.na=%s, achieved power=%.3f\n",
            n_donors, is.na(n_donors), res$ssize[, "power"]))

cat("\n=== Cross-check: does this donor route actually beat cell-level testing (the Skill's core claim)? ===\n")
# Cell-level test: treat each cell as an independent replicate (the WRONG way, per the Skill)
# using a simple two-sample comparison per gene on log1p-normalized counts, BH-corrected.
disease_cells <- do.call(cbind, cell_counts[donor_condition == "disease"])
control_cells <- do.call(cbind, cell_counts[donor_condition == "control"])
libsize_d <- colSums(disease_cells); libsize_c <- colSums(control_cells)
norm_d <- sweep(disease_cells, 2, libsize_d / mean(c(libsize_d, libsize_c)), "/")
norm_c <- sweep(control_cells, 2, libsize_c / mean(c(libsize_d, libsize_c)), "/")
log_d <- log1p(norm_d); log_c <- log1p(norm_c)
pvals <- sapply(seq_len(nrow(log_d)), function(g) {
  tryCatch(t.test(log_d[g, ], log_c[g, ])$p.value, error = function(e) NA)
})
padj <- p.adjust(pvals, method = "BH")
called <- which(padj < 0.05)
true_hits <- sum(called %in% true_de_genes)
false_hits <- sum(!(called %in% true_de_genes))
realized_fdr <- if (length(called) > 0) false_hits / length(called) else NA
cat(sprintf("Cell-level testing (treating %d cells as replicates): %d genes called at BH<0.05, realized FDR=%.3f (true DE genes planted: %d)\n",
            ncol(disease_cells) + ncol(control_cells), length(called), realized_fdr, length(true_de_genes)))
cat(sprintf("Donor-level pseudobulk sizing gives n=%s DONORS for 80%% power -- the Skill's claim that\n", n_donors),
    "cell-level testing inflates false discoveries while pseudobulk is the correct unit is the comparison above.\n")
