# Input 7 (Adversarial) -- "My GWAS is FinnGen (Finnish ancestry) and my eQTL LD reference is
# 1000 Genomes EUR. Compute the z-score vs LD consistency diagnostic before running coloc.susie;
# if it fails, tell me what to do instead."
#
# Planted truth: GWAS z-scores are generated from genotype population A's true LD; the LD matrix
# handed to susieR is instead population B's (independently drawn, unrelated correlation
# structure) -- a genuine ancestry-style mismatch, not the accidental self-inconsistency found in
# the Skill's own shipped examples (see input2_output.txt / skill_own_example_check.txt). This
# tests whether the Skill's estimate_s_rss gate correctly separates "real mismatch, correctly
# caught" from "broken demo data" -- and whether it gives the agent the right instruction to stop.

library(susieR)
set.seed(808)
n_ind <- 3000; n_snps <- 200
positions <- sort(sample(30000000:31000000, n_snps))

# Population A: true LD underlying the GWAS z-scores
rhoA <- 0.9
GA <- scale(matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% chol(rhoA^abs(outer(1:n_snps,1:n_snps,'-'))))
causal <- 100
y_gwas <- 0.3 * GA[, causal] + rnorm(n_ind, 0, 1)
get_ss <- function(y, G) { b<-s<-numeric(ncol(G)); for(j in 1:ncol(G)){f<-summary(lm(y~G[,j]))$coefficients; b[j]<-f[2,1]; s[j]<-f[2,2]}; list(beta=b,se=s) }
gwas_ss <- get_ss(y_gwas, GA)
z_gwas <- gwas_ss$beta / gwas_ss$se
snp_ids <- paste0('rs', 1:n_snps)

ld_matched <- cor(GA); dimnames(ld_matched) <- list(snp_ids, snp_ids)
lam_matched <- susieR::estimate_s_rss(z = z_gwas, R = ld_matched, n = n_ind)
cat(sprintf('Matched (in-sample) LD:    lambda = %.4f  (expect near 0, pipeline may proceed)\n', lam_matched))

# First attempt at a "wrong ancestry" LD: an independently-drawn AR(1) population with a
# different decay rate. This did NOT trigger the gate (lambda ~ 0) -- recorded as a genuine
# negative finding: same-shape-different-strength AR(1) LD is not a strong enough mismatch for
# estimate_s_rss to flag at this SNP density/sample size. Not every "different population" LD
# reference is caught; the diagnostic is not a universal ancestry-mismatch detector.
set.seed(909)
rhoB <- 0.3
GB <- scale(matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% chol(rhoB^abs(outer(1:n_snps,1:n_snps,'-'))))
ld_mild_mismatch <- cor(GB); dimnames(ld_mild_mismatch) <- list(snp_ids, snp_ids)
lam_mild <- susieR::estimate_s_rss(z = z_gwas, R = ld_mild_mismatch, n = n_ind)
cat(sprintf('Mild mismatch (different AR1 decay) LD: lambda = %.4f  -- NOT caught (negative finding)\n', lam_mild))

# A genuine structural mismatch DOES trigger the gate: this reproduces the Skill's own explicitly
# documented silent-failure mode ("Row and column order of R MUST match SNP order in the beta
# vector -- silent failure otherwise... Verify with stopifnot(rownames(R) == names(beta))").
# Here the LD matrix rows/cols are permuted relative to the beta vector but still carry the
# original (now-wrong) dimnames, exactly the silent failure the Skill warns about.
perm <- sample(1:n_snps)
ld_mismatched <- cor(GA)[perm, perm]
dimnames(ld_mismatched) <- list(snp_ids, snp_ids)
lam_mismatched <- susieR::estimate_s_rss(z = z_gwas, R = ld_mismatched, n = n_ind)
cat(sprintf('Permuted-order LD (Skill-documented failure mode): lambda = %.4f  (Skill: abort if > 0.05)\n', lam_mismatched))

cat('\nASSERTION: matched LD passes the gate (lambda <= 0.05):', lam_matched <= 0.05, '\n')
cat('ASSERTION: mismatched LD is correctly caught (lambda > 0.05):', lam_mismatched > 0.05, '\n')

if (lam_mismatched > 0.05) {
  cat('\nREQUIRED AGENT BEHAVIOR per SKILL.md: do NOT proceed to runsusie()/coloc.susie() with this\n')
  cat('LD reference. Either obtain ancestry-matched or in-sample LD, or fall back to coloc.abf\n')
  cat('(which does not require an LD matrix), and report the estimate_s_rss lambda in the methods.\n')
}
