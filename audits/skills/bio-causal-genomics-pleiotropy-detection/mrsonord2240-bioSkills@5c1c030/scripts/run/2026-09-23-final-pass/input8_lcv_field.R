# Input 8 (NEW -- not in the pre-fix 7) -- "Compute LCV gcp from LDSC-merged sumstats to
# distinguish causation from pure genetic correlation" (one of usage-guide.md's own
# Example Prompts, never executed as a scored input in the pre-fix audit -- pre-fix only
# used a throwaway verification script, run/test_lcv.R, not counted toward the 7 scored
# inputs). Directly re-runs the P1 fix: SKILL.md's LCV section changed
# `res_lcv$gcp` -> `res_lcv$gcp.pm` (`res_lcv$gcp` silently returns NULL; it is not an
# error, so an agent copying the old snippet would not notice anything was wrong until
# it printed NULL where a number was expected).

setwd('F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/src/LCV/R')
set.seed(1)
m <- 2000
ell <- runif(m, 1, 50)
rho_true <- 0.3
z1 <- rnorm(m, 0, sqrt(ell))
z2 <- rho_true * z1 + rnorm(m, 0, sqrt(ell))
source('RunLCV.R')
res_lcv <- RunLCV(ell, z1, z2, no.blocks = 20)

cat('Fields actually returned by RunLCV():\n')
print(names(res_lcv))

cat('\n=== Testing the CURRENT SKILL.md snippet ===\n')
cat('SKILL.md now reads:\n')
cat('  res_lcv$gcp.pm (posterior mean gcp; there is no res_lcv$gcp field); res_lcv$pval.gcpzero.2tailed\n\n')

gcp_pm <- res_lcv$gcp.pm
gcp_old_field <- res_lcv$gcp  # the OLD (pre-fix) SKILL.md snippet
pval <- res_lcv$pval.gcpzero.2tailed

cat('res_lcv$gcp.pm =', gcp_pm, '  (current SKILL.md field -- works)\n')
cat('res_lcv$gcp    =', if (is.null(gcp_old_field)) 'NULL' else gcp_old_field,
    ' (OLD SKILL.md field -- silently NULL, would have been a downstream bug, not a crash)\n')
cat('res_lcv$pval.gcpzero.2tailed =', pval, ' (unchanged; was already correct)\n')

cat('\n=== Regression verdict ===\n')
if (!is.null(gcp_pm) && is.numeric(gcp_pm) && is.null(gcp_old_field)) {
  cat('CONFIRMED: gcp.pm is a real numeric field; the old `gcp` field genuinely does not exist (NULL).\n')
  cat('The fixed SKILL.md snippet (res_lcv$gcp.pm) now matches the actual RunLCV() return object.\n')
} else {
  cat('UNEXPECTED: field behavior differs from what the fix log claims -- flag for re-review.\n')
}

cat('\n=== gcp interpretation table sanity check (moved into SKILL.md LCV section by the redundancy pass) ===\n')
cat('gcp.pm =', round(gcp_pm, 3), '-> ', if (abs(gcp_pm) < 0.35) 'closer to 0 (partial causation/mixture region)' else if (abs(gcp_pm) < 0.8) 'closer to 0.5-0.6 (partial causation, modest direction)' else 'closer to 1 (fully causal in tested direction)', '\n')
