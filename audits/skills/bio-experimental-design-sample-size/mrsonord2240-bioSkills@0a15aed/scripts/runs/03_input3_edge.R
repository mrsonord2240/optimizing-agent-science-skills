# Input 3 (Edge) — regression of pre-fix Input 3.
# Prompt: "My grant only funds 6 per group at 1.5-fold, disp 0.2, FDR 0.05. What power
# and true FDR does that give? Separately, a reviewer wants 90% power at a 1.2-fold
# change under the same dispersion -- is that reachable at any fundable n?"
suppressPackageStartupMessages(library(ssizeRNA))

cat("=== Part A: check.power at budget-fixed n=6 ===\n")
set.seed(20260918)
cp <- check.power(nGenes = 20000, pi0 = 0.95, m = 6, mu = 200, disp = 0.2,
                  fc = 1.5, fdr = 0.05, sims = 50)
print(cp)
if (is.nan(cp$fdr_bh_ave)) {
  cat(sprintf("At n=6/group: BH average power = %.3f, true FDR = NaN (zero discoveries, per SKILL.md's guidance)\n",
              cp$pow_bh_ave))
} else {
  cat(sprintf("At n=6/group: BH average power = %.3f, true FDR = %.3f\n", cp$pow_bh_ave, cp$fdr_bh_ave))
}

cat("\n=== Part B: is the stop-condition guard code actually present & functional? ===\n")
cat("Testing SKILL.md's literal guard: n <- res$ssize[, 'ssize']; if (is.na(n)) stop(...)\n")
set.seed(20260918)
# Deliberately reachable-but-tiny maxN to force NA, mimicking an infeasible target
res_infeasible <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200,
                                   mu = 200, disp = 0.8,   # high dispersion
                                   fc = 1.2, fdr = 0.05, power = 0.90,
                                   maxN = 200)
n <- res_infeasible$ssize[, "ssize"]
cat(sprintf("At disp=0.8, fc=1.2, target power=0.90, maxN=200: n=%s\n", n))
guard_result <- tryCatch({
  if (is.na(n)) stop("no n <= maxN reaches the target; raise maxN or revise fc/dispersion")
  "no stop triggered"
}, error = function(e) paste("STOP triggered as SKILL.md documents:", conditionMessage(e)))
cat(guard_result, "\n")

cat("\n=== Part C: is the 1.2-fold/90%-power target reachable at ANY practically fundable n? ===\n")
set.seed(20260918)
res_big <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200, mu = 200, disp = 0.8,
                           fc = 1.2, fdr = 0.05, power = 0.90, maxN = 1000)
n_big <- res_big$ssize[, "ssize"]
cat(sprintf("Raised maxN to 1000: n=%s\n", n_big))
if (is.na(n_big)) cat("Still unreachable even at maxN=1000 -- SKILL.md's fallback (report achieved power at\n",
                       "practically fundable maxN, or sweep fc instead) is the only honest answer here.\n")
