# Input 5 (Stress): "ANGPTL3 has two independent cis-pQTLs in low LD. Run coloc.susie on the cis-
# window with in-sample LD, report per-credible-set PP.H4 against triglycerides GWAS, and run a Wald
# ratio per credible set. Also run the robust/penalized correlated-instrument cis-IVW as a sensitivity
# check."
#
# SYNTHETIC individual-level genotypes (not summary stats) so the LD matrix and z-scores used by
# susie_rss are internally consistent (a real requirement runsusie enforces: "d must include LD...and
# N"). Two independent causal SNPs planted in low mutual LD, each with its own true effect on protein
# and (via the protein) on triglycerides -- allelic heterogeneity, the scenario coloc.abf alone cannot
# resolve per-signal.

suppressPackageStartupMessages({ library(coloc); library(MendelianRandomization); library(TwoSampleMR) })
set.seed(31415)

n_ind <- 4000
n_snp <- 30
maf <- runif(n_snp, 0.1, 0.4)
G <- sapply(maf, function(p) rbinom(n_ind, 2, p))  # independent genotypes at baseline
causal1 <- 6L; causal2 <- 22L  # far apart -> low mutual LD by construction

# Induce local LD blocks around each causal SNP by mixing in a shared latent block genotype
block1 <- rbinom(n_ind, 2, maf[causal1])
block2 <- rbinom(n_ind, 2, maf[causal2])
for (j in 1:n_snp) {
  if (abs(j - causal1) <= 3) G[, j] <- round(0.7*G[, j] + 0.3*block1)
  if (abs(j - causal2) <= 3) G[, j] <- round(0.7*G[, j] + 0.3*block2)
}
G <- pmin(pmax(G, 0), 2)
snp_id <- sprintf("rs%07d", 6000000 + seq_len(n_snp))
colnames(G) <- snp_id

ld <- cor(G)
cat("Mutual LD between the two planted causal SNPs (r):", round(ld[causal1, causal2], 3), "\n")

# Two independent causal effects on protein level (opposite directions -- distinct biology per signal)
beta1_true <- 0.30; beta2_true <- -0.25
protein <- 0.30 * scale(G[, causal1])[,1] + (-0.25) * scale(G[, causal2])[,1] + rnorm(n_ind, 0, 1)
# Outcome (triglycerides) driven ONLY through the protein (shared MR effect for both signals)
true_mr_effect <- 0.5
trig <- true_mr_effect * protein + rnorm(n_ind, 0, 1)

get_sumstats <- function(y) {
  t(sapply(seq_len(n_snp), function(j) {
    f <- lm(y ~ G[, j])
    s <- summary(f)$coefficients[2, 1:2]
    c(beta = unname(s[1]), se = unname(s[2]))
  }))
}
ss_protein <- get_sumstats(protein); ss_trig <- get_sumstats(trig)

pqtl <- data.frame(SNP=snp_id, BETA=ss_protein[,"beta"], SE=ss_protein[,"se"], P = 2*pnorm(-abs(ss_protein[,"beta"]/ss_protein[,"se"])))
trigdf <- data.frame(SNP=snp_id, BETA=ss_trig[,"beta"], SE=ss_trig[,"se"], P = 2*pnorm(-abs(ss_trig[,"beta"]/ss_trig[,"se"])))
cat("Cis-pQTL P-values at the two planted loci: causal1 P=", format(pqtl$P[causal1], scientific=TRUE),
    " causal2 P=", format(pqtl$P[causal2], scientific=TRUE), "\n")

# ---- coloc.susie per dataset (needs LD + N) ----
d1 <- list(beta = pqtl$BETA, varbeta = pqtl$SE^2, snp = snp_id, type = "quant", N = n_ind, sdY = sd(protein), LD = ld)
d2 <- list(beta = trigdf$BETA, varbeta = trigdf$SE^2, snp = snp_id, type = "quant", N = n_ind, sdY = sd(trig), LD = ld)

s1 <- runsusie(d1, suffix = 1)
s2 <- runsusie(d2, suffix = 2)
cat("\nProtein susie credible sets:", length(s1$sets$cs), "\n")
cat("Triglyceride susie credible sets:", length(s2$sets$cs), "\n")

susie_res <- tryCatch(coloc.susie(s1, s2), error = function(e) { cat("coloc.susie ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(susie_res)) {
  cat("\n-- coloc.susie per-credible-set-pair summary --\n")
  print(susie_res$summary[, c("nsnps","hit1","hit2","PP.H0.abf","PP.H3.abf","PP.H4.abf")])
}

# ---- Per-signal Wald ratio at each planted sentinel ----
for (cidx in c(causal1, causal2)) {
  b_x <- pqtl$BETA[cidx]; se_x <- pqtl$SE[cidx]
  b_y <- trigdf$BETA[cidx]; se_y <- trigdf$SE[cidx]
  wald_b <- b_y / b_x
  wald_se <- se_y / abs(b_x)
  cat(sprintf("\nWald ratio at %s (planted signal): b=%.4f se=%.4f (ground-truth MR effect=%.2f)\n",
              snp_id[cidx], wald_b, wald_se, true_mr_effect))
}

# ---- Robust/penalized correlated-instrument cis-IVW sensitivity, using both signal SNPs + neighbours ----
window_idx <- sort(unique(c((causal1-2):(causal1+2), (causal2-2):(causal2+2))))
window_idx <- window_idx[window_idx >= 1 & window_idx <= n_snp]
sub_sig <- pqtl$P[window_idx] < 0.01  # relaxed threshold for this synthetic small-N stress test
use_idx <- window_idx[sub_sig]
cat("\nInstruments retained for correlated cis-IVW sensitivity:", length(use_idx), "\n")
if (length(use_idx) >= 2) {
  ld_sub <- ld[use_idx, use_idx]
  mr_obj <- mr_input(bx = pqtl$BETA[use_idx], bxse = pqtl$SE[use_idx],
                      by = trigdf$BETA[use_idx], byse = trigdf$SE[use_idx],
                      correlation = ld_sub)
  # BUG FOUND (recorded as a P1 finding, not silently worked around): with coloc, MendelianRandomization,
  # and TwoSampleMR all loaded, `library()` order determines which `mr_ivw` is on the search path.
  # TwoSampleMR::mr_ivw is a plain function with signature (b_exp, b_out, se_exp, se_out, parameters);
  # MendelianRandomization::mr_ivw is an S4 generic dispatching on MRInput. Loading order
  # coloc -> MendelianRandomization -> TwoSampleMR (TwoSampleMR last) masks the S4 generic and calling
  # `mr_ivw(mr_obj, model='default', correl=TRUE)` as SKILL.md's own "Cis-IVW with Correlated
  # Instruments" section instructs throws `Error: unused arguments (model = "default", correl = TRUE)`
  # -- a confusing error that gives no hint the real cause is namespace masking, not a bad call.
  # Reproduced in isolation: debug_mrivw3.R in this run/ folder. SKILL.md never warns about this and
  # its two adjacent code blocks (main cis-MR workflow loads TwoSampleMR; correlated-IVW block loads
  # MendelianRandomization) are silently order-dependent if combined into one script, which an agent
  # naturally does when executing an end-to-end analysis. Using explicit `MendelianRandomization::`
  # namespacing below is the correct fix and what SKILL.md should instruct.
  std_correl <- MendelianRandomization::mr_ivw(mr_obj, model = "default", correl = TRUE)
  robust_correl <- MendelianRandomization::mr_ivw(mr_obj, model = "default", correl = TRUE, robust = TRUE, penalized = TRUE)
  cat("Standard correlated cis-IVW:  b=", round(std_correl@Estimate,4), " se=", round(std_correl@StdError,4), "\n")
  cat("Robust+penalized cis-IVW:     b=", round(robust_correl@Estimate,4), " se=", round(robust_correl@StdError,4), "\n")
  cat("Ground-truth shared MR effect (both signals):", true_mr_effect, "\n")
}
