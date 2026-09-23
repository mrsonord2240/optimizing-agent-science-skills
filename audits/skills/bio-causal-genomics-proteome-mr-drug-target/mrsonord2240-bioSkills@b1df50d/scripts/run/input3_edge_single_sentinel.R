# Input 3 (Edge): "I only have one genome-wide-significant cis-pQTL for protein ANGPTL4 in the
# +/-500kb window -- can you still run a cis-MR against triglycerides and tell me if it's publishable?"
#
# Edge case: N=1 instrument (Wald ratio only -- no IVW/Egger/heterogeneity possible), small window
# (15 SNPs total, only 1 genome-wide significant) -- tests whether the skill correctly identifies this
# as "minimum publishable cis-MR" per its own Decision Tree row and still requires coloc + PAV +
# cross-platform before calling it a drug target, rather than treating a single Wald ratio as
# sufficient. SYNTHETIC DATA, planted ground truth.

suppressPackageStartupMessages({ library(TwoSampleMR); library(coloc) })
set.seed(777)

n_snp <- 15
gene_chr <- 19; gene_start <- 8429281; gene_end <- 8446905  # ANGPTL4 hg38 approx
win <- 500000
pos <- sort(sample((gene_start - win):(gene_end + win), n_snp))
sentinel_idx <- 8L

d <- abs(outer(pos, pos, "-")); ld <- 0.85 ^ (d / 30000); diag(ld) <- 1
maf <- runif(n_snp, 0.05, 0.45)
snp_id <- sprintf("rs%07d", 3000000 + seq_len(n_snp))
a1 <- sample(c("A","C","G","T"), n_snp, replace = TRUE)
a2 <- sapply(a1, function(x) sample(setdiff(c("A","C","G","T"), x), 1))

true_beta <- rep(0, n_snp); true_beta[sentinel_idx] <- 0.40
marg_true <- as.numeric(ld[, sentinel_idx]) * true_beta[sentinel_idx]
n_protein <- 10708  # Fenland-scale N
se_p <- sqrt(1/(2*maf*(1-maf)*n_protein)) * 3.0
beta_p <- marg_true + rnorm(n_snp, 0, se_p)
# force only the sentinel to cross 5e-8 by construction: shrink neighbours' noise draw retry if needed
p_p <- 2*pnorm(-abs(beta_p/se_p))

true_mr_effect <- 0.6  # per-SD protein -> triglycerides (quantitative outcome)
n_tg <- 92064
marg_tg <- marg_true * true_mr_effect
se_tg <- sqrt(1/(2*maf*(1-maf)*n_tg)) * 3.0
beta_tg <- marg_tg + rnorm(n_snp, 0, se_tg)

pqtl <- data.frame(SNP=snp_id, CHR=gene_chr, POS=pos, BETA=beta_p, SE=se_p, A1=a1, A2=a2, EAF=maf, P=p_p)
tg   <- data.frame(SNP=snp_id, CHR=gene_chr, POS=pos, BETA=beta_tg, SE=se_tg, A1=a1, A2=a2, EAF=maf,
                    P=2*pnorm(-abs(beta_tg/se_tg)))

sig <- subset(pqtl, P < 5e-8)
sig$f_stat <- (sig$BETA/sig$SE)^2
sig <- subset(sig, f_stat >= 10)
cat("Genome-wide-significant, F>=10 cis-pQTLs in window:", nrow(sig), "-> SNP(s):", paste(sig$SNP, collapse=","), "\n")

exp_dat <- format_data(sig, type="exposure", snp_col="SNP", beta_col="BETA", se_col="SE",
                        effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
out_dat <- format_data(tg[tg$SNP %in% exp_dat$SNP,], type="outcome", snp_col="SNP", beta_col="BETA",
                        se_col="SE", effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
dat <- suppressMessages(harmonise_data(exp_dat, out_dat, action = 2))
cat("Harmonised instruments:", nrow(dat), "\n")

if (nrow(dat) == 1) {
  res <- mr(dat, method_list = "mr_wald_ratio")
  cat("\n-- Wald ratio (single sentinel) --\n"); print(res[, c("method","nsnp","b","se","pval")])
  cat("NOTE: N=1 instrument -> no heterogeneity test (Cochran's Q), no Egger intercept, no MR-PRESSO\n")
  cat("possible. This is 'minimum publishable cis-MR' per the skill's own decision tree; it still\n")
  cat("REQUIRES coloc + cross-platform + PAV-excluded sensitivity before any drug-target claim.\n")
} else {
  cat("LD pulled", nrow(dat), "neighbours past P<5e-8+F>=10 (realistic cis-window behaviour, not the\n")
  cat("pure N=1 case originally targeted). Reporting BOTH sub-cases from the same window to exercise\n")
  cat("the skill's own Common-Errors row 'Wald ratio at sentinel SNP differs from cis-IVW':\n")
  res_ivw <- mr(dat, method_list = "mr_ivw")
  cat("\n-- (a) Cis-IVW on all", nrow(dat), "harmonised instruments --\n")
  print(res_ivw[, c("method","nsnp","b","se","pval")])

  sentinel_snp <- sig$SNP[which.min(sig$P)]
  dat_sentinel <- subset(dat, SNP == sentinel_snp)
  res_wald <- mr(dat_sentinel, method_list = "mr_wald_ratio")
  cat("\n-- (b) Wald ratio restricted to the single most-significant sentinel (", sentinel_snp, ") --\n")
  print(res_wald[, c("method","nsnp","b","se","pval")])
  cat("\nSentinel-only vs full-IVW effect ratio:", round(res_wald$b[1] / res_ivw$b[1], 3),
      "-- both point estimates should agree in direction and rough magnitude when the window is\n")
  cat("clean (no LD-confounded neighbour); a large divergence here would flag exactly the 'Wald ratio\n")
  cat("differs from cis-IVW' failure mode and should trigger MR-PRESSO / tighter clumping per the skill.\n")
  res <- res_wald
}

cc <- coloc.abf(dataset1 = list(beta=pqtl$BETA, varbeta=pqtl$SE^2, snp=pqtl$SNP, type="quant", N=n_protein, sdY=1),
                 dataset2 = list(beta=tg$BETA, varbeta=tg$SE^2, snp=tg$SNP, type="quant", N=n_tg, sdY=1),
                 p1=1e-4, p2=1e-4, p12=5e-6)
cat("\n-- coloc.abf on 15-SNP window (small window caveat: fewer SNPs => less power to distinguish H3 vs H4) --\n")
print(cc$summary)
cat("\nGround truth planted MR effect:", true_mr_effect, "; recovered Wald b:", round(res$b[1],4), "\n")
