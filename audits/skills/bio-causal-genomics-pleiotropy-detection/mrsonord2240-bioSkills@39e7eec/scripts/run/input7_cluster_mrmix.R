# Input 7 (Adversarial, REGRESSION of pre-fix Input 7) -- "I suspect my exposure's 18
# instruments operate through two distinct mechanisms. Run MR-Clust to find the
# clusters, and also run MR-Mix and contamination mixture as a cross-check." n=18 is
# deliberately BELOW the documented MR-Mix/conmix/MR-Clust minimum of 20. Tests whether
# the CURRENT SKILL.md's rewritten Common Errors row (now describing the real
# non-NA-but-unreliable behavior, plus a pre-flight n-check recommendation) matches
# actual package behavior and whether an agent following it now flags the result rather
# than reporting the numbers uncaveated. Ground truth: two clusters at causal effect
# ~0.2 (9 SNPs) and ~0.6 (9 SNPs).

library(mrclust)
library(MRMix)
library(MendelianRandomization)

dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_clusters.rds')
cat('n SNPs:', nrow(dat), '(SKILL.md: MR-Mix / contamination mixture documented minimum is 20)\n\n')

cat('=== Pre-flight n-check (per the fixed SKILL.md Common Errors row) ===\n')
if (nrow(dat) < 20) {
  cat('WARNING: n=', nrow(dat), '< 20. Per SKILL.md: "Check n before trusting the output: below 20 SNPs,\n')
  cat('  treat MR-Mix / conmix point estimates and CIs as unreliable regardless of apparent significance."\n\n')
}

cat('=== MR-Clust ===\n')
ratio_hat <- dat$beta.outcome / dat$beta.exposure
ratio_se  <- abs(dat$se.outcome / dat$beta.exposure)
res_mc <- mr_clust_em(theta = ratio_hat, theta_se = ratio_se,
                       bx = dat$beta.exposure, by = dat$beta.outcome,
                       bxse = dat$se.exposure, byse = dat$se.outcome,
                       obs_names = dat$SNP)
per_cluster <- res_mc$results$best
print(table(per_cluster$cluster_class))
cluster_means <- aggregate(cluster_mean ~ cluster_class, data = per_cluster, FUN = function(x) round(unique(x), 3))
print(cluster_means)
cat('Ground truth cluster means: ~0.2 and ~0.6\n')

cat('\n=== MR-Mix (n=18 < documented minimum of 20) ===\n')
mrmix_res <- tryCatch(
  MRMix(dat$beta.exposure, dat$beta.outcome, dat$se.exposure, dat$se.outcome),
  error = function(e) { cat('MR-Mix ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(mrmix_res)) {
  cat('theta:', mrmix_res$theta, ' SE:', mrmix_res$SE, ' pvalue:', mrmix_res$pvalue, '\n')
  if (is.na(mrmix_res$theta)) {
    cat('MR-Mix returned NA below its ~20-SNP minimum.\n')
  } else {
    cat('MR-Mix returned a NON-NA point estimate below its documented 20-SNP minimum --\n')
    cat('  matches the CURRENT (fixed) SKILL.md Common Errors row, which now says this is the real behavior\n')
    cat('  ("a confident point estimate below the 20-SNP minimum, not NA") and instructs treating it as unreliable.\n')
  }
}

cat('\n=== Contamination mixture (n=18 < documented minimum of 20) ===\n')
mr_obj <- mr_input(bx = dat$beta.exposure, bxse = dat$se.exposure,
                    by = dat$beta.outcome, byse = dat$se.outcome, snps = dat$SNP)
conmix <- tryCatch(mr_conmix(mr_obj), error = function(e) { cat('conmix ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(conmix)) cat('Estimate:', round(conmix@Estimate, 4), ' 95% CI:', round(conmix@CILower,4), 'to', round(conmix@CIUpper,4), '\n')
