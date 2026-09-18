# Input 1 (Canonical) — regression of pre-fix Input 1.
# Prompt: "I'm running a bulk RNA-seq experiment, tumor vs normal, ~20,000 genes,
# expect 5% DE at fold-change 1.5, dispersion around 0.2 from the literature.
# How many biological replicates per group do I need at 80% power, FDR 0.05?"
#
# Runs SKILL.md's own "FDR-Aware NB Sample Size" scalar block verbatim (the P0-1 fix
# target), then re-runs the ORIGINAL failing call (ssizeRNA_vary with scalars) as a
# negative-control regression check that the documented error still fires exactly as
# SKILL.md now warns, so the warning is not stale.
suppressPackageStartupMessages(library(ssizeRNA))

cat("=== Part A: SKILL.md's scalar route (ssizeRNA_single) ===\n")
set.seed(20260918)
res <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200,
                       mu = 200, disp = 0.2,
                       fc = 1.5, fdr = 0.05, power = 0.80,
                       maxN = 200)
print(res$ssize)
n <- res$ssize[, "ssize"]
cat(sprintf("n = %s, is.na = %s\n", n, is.na(n)))

cat("\n=== Part A2: repeat 5x unseeded to check drift (T3 determinism) ===\n")
ns <- sapply(1:5, function(i) {
  r <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200, mu = 200, disp = 0.2,
                        fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)
  r$ssize[, "ssize"]
})
cat("5 unseeded n values:", paste(ns, collapse = ", "), "\n")
cat("range:", min(ns), "-", max(ns), "\n")

cat("\n=== Part B: NEGATIVE CONTROL - ssizeRNA_vary with SCALARS (should still error) ===\n")
result_B <- tryCatch({
  ssizeRNA_vary(nGenes = 20000, pi0 = 0.95, mu = 200, disp = 0.2,
               fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)
  "NO ERROR - REGRESSION: warning is now stale"
}, error = function(e) paste("ERROR (expected):", conditionMessage(e)))
cat(result_B, "\n")

cat("\n=== Part C: sensitivity to fold change, matches SKILL.md's own claim ===\n")
for (fc in c(1.5, 2, 3)) {
  r <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200, mu = 200, disp = 0.2,
                       fc = fc, fdr = 0.05, power = 0.80, maxN = 200)
  cat(sprintf("fc=%.1f -> n=%s\n", fc, r$ssize[, "ssize"]))
}
