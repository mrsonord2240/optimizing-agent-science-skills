# Input 2 (Variant A): "I have a 4-sample pilot. Estimate dispersions with DESeq2 and use
# them to size the full study."  -- the SKILL.md 'Pilot Dispersions Drive Honest Sample Size'
# block, run verbatim on SYNTHETIC pilots whose TRUE dispersion is 0.35.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
pdf(NULL)
suppressPackageStartupMessages({library(DESeq2); library(edgeR); library(ssizeRNA)})
set.seed(20260916)
D <- "F:/OpenScience/audits/bio-experimental-design-sample-size/data"
TRUE_DISP <- 0.35

pilot_disp <- function(tag) {
  counts <- as.matrix(read.csv(file.path(D, sprintf("SYNTHETIC_pilot_%s_counts.csv", tag)), row.names = 1))
  col    <- read.csv(file.path(D, sprintf("SYNTHETIC_pilot_%s_coldata.csv", tag)), row.names = 1)
  col$condition <- factor(col$condition)
  ## ---- SKILL.md block, verbatim ----
  dds <- DESeqDataSetFromMatrix(counts, col, ~ condition)
  dds <- DESeq(dds, quiet = TRUE)
  disp <- dispersions(dds)
  cat(sprintf("\n=== pilot %s (n=%d/group) : DESeq2 dispersions(dds) ===\n", tag, ncol(counts)/2))
  print(summary(disp[is.finite(disp)]))
  ## ---- what the SKILL.md tells you to feed forward: "median/trend" ----
  med <- median(disp[is.finite(disp)])
  cat(sprintf("  median DESeq2 dispersion = %.4f   (TRUE = %.2f;  ratio %.2fx)\n",
              med, TRUE_DISP, med/TRUE_DISP))
  # edgeR cross-check (the SKILL.md offers DESeq2 *or* edgeR)
  y <- DGEList(counts, group = col$condition); y <- calcNormFactors(y)
  y <- estimateDisp(y, model.matrix(~condition, col))
  cat(sprintf("  edgeR common=%.4f  trended(median)=%.4f  tagwise(median)=%.4f\n",
              y$common.dispersion, median(y$trended.dispersion), median(y$tagwise.dispersion)))
  mu <- rowMeans(counts(dds, normalized = TRUE))
  list(disp = disp, mu = mu, med = med, edgeR_common = y$common.dispersion)
}

p2 <- pilot_disp("2v2")
p6 <- pilot_disp("6v6")

cat("\n=== Size the full study from each pilot (ssizeRNA_vary with mu/disp VECTORS, per SKILL.md) ===\n")
size_from <- function(p, lbl) {
  ok <- is.finite(p$disp) & is.finite(p$mu) & p$mu > 0
  r <- tryCatch(ssizeRNA_vary(nGenes = sum(ok), pi0 = 0.95, mu = p$mu[ok], disp = p$disp[ok],
                              fc = 1.5, fdr = 0.05, power = 0.80, maxN = 30),
                error = function(e) paste("ERROR:", conditionMessage(e)))
  if (is.list(r)) cat(sprintf("  %-26s -> n = %s per group\n", lbl, r$ssize))
  else            cat(sprintf("  %-26s -> %s\n", lbl, r))
  invisible(r)
}
set.seed(1); size_from(p2, "from 2v2 pilot")
set.seed(1); size_from(p6, "from 6v6 pilot")
cat("\n  reference: scalar TRUE dispersion 0.35 at the pilot's mean depth\n")
set.seed(1); r <- tryCatch(ssizeRNA_vary(nGenes=12000, pi0=0.95, mu=median(p6$mu), disp=TRUE_DISP,
                                         fc=1.5, fdr=0.05, power=0.80, maxN=30),
                           error=function(e) paste("ERROR:", conditionMessage(e)))
if (is.list(r)) cat(sprintf("  %-26s -> n = %s per group\n", "from TRUE disp = 0.35", r$ssize)) else cat("  ", r, "\n")
