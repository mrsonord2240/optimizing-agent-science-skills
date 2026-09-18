# Input 2 (Variant A) — regression of pre-fix Input 2.
# Prompt: "I have a 4-sample (2v2) pilot from my own SYNTHETIC dataset (planted dispersion
# 0.30). Estimate dispersions with DESeq2 and use them to size the full study with
# ssizeRNA_vary."
suppressPackageStartupMessages({
  library(DESeq2)
  library(ssizeRNA)
})

counts_2v2 <- as.matrix(read.csv("data/pilot_2v2_counts.csv", row.names = 1))
coldata_2v2 <- read.csv("data/pilot_2v2_coldata.csv", row.names = 1)
counts_6v6 <- as.matrix(read.csv("data/pilot_6v6_counts.csv", row.names = 1))
coldata_6v6 <- read.csv("data/pilot_6v6_coldata.csv", row.names = 1)

run_pilot <- function(counts, coldata, label) {
  cat(sprintf("\n=== %s ===\n", label))
  set.seed(20260918)
  dds <- DESeqDataSetFromMatrix(counts, coldata, ~ condition)
  dds <- DESeq(dds)
  disp_vec <- dispersions(dds)
  mu_vec <- rowMeans(counts(dds, normalized = TRUE))
  keep <- is.finite(disp_vec) & is.finite(mu_vec) & mu_vec > 0
  disp_vec <- disp_vec[keep]; mu_vec <- mu_vec[keep]
  cat("Dispersion summary (planted 0.30):\n")
  print(summary(disp_vec))
  cat(sprintf("Median dispersion: %.3f (ratio to planted 0.30: %.2fx)\n",
              median(disp_vec), median(disp_vec) / 0.30))

  set.seed(20260918)
  res <- ssizeRNA_vary(nGenes = length(mu_vec), pi0 = 0.95,
                       mu = mu_vec, disp = disp_vec,
                       fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)
  n <- res$ssize[, "ssize"]
  cat(sprintf("ssizeRNA_vary result: n=%s, is.na=%s, achieved power=%.3f\n",
              n, is.na(n), res$ssize[, "power"]))
  invisible(n)
}

n_2v2 <- run_pilot(counts_2v2, coldata_2v2, "2v2 pilot -> DESeq2 -> ssizeRNA_vary")
n_6v6 <- run_pilot(counts_6v6, coldata_6v6, "6v6 pilot -> DESeq2 -> ssizeRNA_vary")

cat(sprintf("\nCross-check against SKILL.md's stated range ('mid-40s to 74' at fc=1.5): 2v2 n=%s, 6v6 n=%s\n",
            n_2v2, n_6v6))
