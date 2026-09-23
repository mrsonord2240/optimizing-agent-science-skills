# Input 2 (Variant A): "Test IL6R protein -> rheumatoid arthritis using cis-pQTLs from deCODE
# SomaScan plus colocalization. Flag any cis-pQTL coloc'd with neighbouring genes' eQTLs in GTEx whole
# blood. Also replicate on UKB-PPP Olink and report cross-platform agreement."
#
# SYNTHETIC DATA, planted ground truth. Two platforms simulated for the same locus:
#  - Olink (UKB-PPP-style, N=54219): true causal SNP drives both protein and RA risk.
#  - SomaScan (deCODE-style, N=35559): the SAME causal SNP drives protein+RA, but ONE extra SNP is a
#    coding (missense) variant that creates a large SomaScan-only aptamer-affinity artifact (an
#    "AAVQTL") with NO true effect on RA -- this is the Eldjarn 2023 platform-discordance mechanism the
#    SKILL.md describes. The test is whether cis-MR + PAV annotation correctly identifies and excludes
#    the artifact rather than accepting it as real signal.

suppressPackageStartupMessages({ library(TwoSampleMR); library(coloc) })
set.seed(4242)

n_snp <- 40
gene_chr <- 1; gene_start <- 154405475; gene_end <- 154469712  # IL6R hg38 approx
win <- 500000
pos <- sort(sample((gene_start - win):(gene_end + win), n_snp))
causal_idx <- 20L
pav_artifact_idx <- 21L   # adjacent SNP, SomaScan-only artifact

d <- abs(outer(pos, pos, "-")); ld <- 0.9 ^ (d / 20000); diag(ld) <- 1
maf <- runif(n_snp, 0.05, 0.45)
snp_id <- sprintf("rs%07d", 2000000 + seq_len(n_snp))
a1 <- sample(c("A","C","G","T"), n_snp, replace = TRUE)
a2 <- sapply(a1, function(x) sample(setdiff(c("A","C","G","T"), x), 1))

true_beta <- rep(0, n_snp); true_beta[causal_idx] <- -0.30  # IL6R inhibition-like: lower protein
marg_true <- as.numeric(ld[, causal_idx]) * true_beta[causal_idx]
true_mr_effect <- -0.55  # protective log-OR direction consistent with tocilizumab (IL6R blockade -> lower RA risk)

make_gwas <- function(n, marg_signal, se_scale, platform_artifact_idx = NULL, artifact_size = 0) {
  se <- sqrt(1/(2*maf*(1-maf)*n)) * se_scale
  beta <- marg_signal + rnorm(n_snp, 0, se)
  if (!is.null(platform_artifact_idx)) beta[platform_artifact_idx] <- beta[platform_artifact_idx] + artifact_size
  p <- 2*pnorm(-abs(beta/se))
  data.frame(SNP=snp_id, CHR=gene_chr, POS=pos, BETA=beta, SE=se, A1=a1, A2=a2, EAF=maf, P=p)
}

# Protein GWAS: Olink clean; SomaScan has the PAV artifact spike at pav_artifact_idx
olink_protein <- make_gwas(54219, marg_true, 3.2)
soma_protein  <- make_gwas(35559, marg_true, 3.6, platform_artifact_idx = pav_artifact_idx, artifact_size = 1.1)

# RA outcome (single, N=58284 EIRA/RACI-scale, case_frac=0.25): true causal path only through protein,
# same outcome used for both platform-specific instrument sets (the artifact has NO effect on RA).
n_ra <- 58284; case_frac <- 0.25
marg_cad <- marg_true * true_mr_effect
se_ra <- sqrt(1/(2*maf*(1-maf)*n_ra*case_frac*(1-case_frac))) * 1.1
beta_ra <- marg_cad + rnorm(n_snp, 0, se_ra)
ra <- data.frame(SNP=snp_id, CHR=gene_chr, POS=pos, BETA=beta_ra, SE=se_ra, A1=a1, A2=a2, EAF=maf,
                  P=2*pnorm(-abs(beta_ra/se_ra)))

vep <- data.frame(SNP = snp_id[pav_artifact_idx], Consequence = "missense_variant")
pav_consequences <- c("missense_variant","stop_gained","stop_lost","frameshift_variant",
                       "splice_acceptor_variant","splice_donor_variant","start_lost","protein_altering_variant")

run_platform <- function(protein_gwas, label, n_protein) {
  sig <- subset(protein_gwas, P < 5e-8)
  sig$f_stat <- (sig$BETA/sig$SE)^2
  sig <- subset(sig, f_stat >= 10)
  sig$is_pav <- sig$SNP %in% vep$SNP[vep$Consequence %in% pav_consequences]
  cat("\n===", label, "=== sig cis-pQTLs:", nrow(sig), " PAV-flagged:", sum(sig$is_pav), "\n")

  exp_dat <- format_data(sig, type="exposure", snp_col="SNP", beta_col="BETA", se_col="SE",
                          effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
  out_dat <- format_data(ra[ra$SNP %in% exp_dat$SNP,], type="outcome", snp_col="SNP", beta_col="BETA",
                          se_col="SE", effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
  dat <- suppressMessages(harmonise_data(exp_dat, out_dat, action = 2))
  primary <- suppressMessages(mr(dat, method_list = if (nrow(dat) >= 10) c("mr_ivw","mr_egger_regression") else "mr_ivw"))
  ivw <- primary[primary$method == "Inverse variance weighted", ]

  dat$is_pav <- dat$SNP %in% vep$SNP[vep$Consequence %in% pav_consequences]
  dat_np <- subset(dat, !is_pav)
  primary_np <- if (nrow(dat_np) >= 1) suppressMessages(mr(dat_np, method_list = "mr_ivw")) else NULL

  cc <- coloc.abf(dataset1 = list(beta=protein_gwas$BETA, varbeta=protein_gwas$SE^2, snp=protein_gwas$SNP,
                                    type="quant", N=n_protein, sdY=1),
                   dataset2 = list(beta=ra$BETA, varbeta=ra$SE^2, snp=ra$SNP, type="cc", N=n_ra, s=case_frac),
                   p1=1e-4, p2=1e-4, p12=5e-6)

  list(label=label, n_instr=nrow(dat), b_all=ivw$b[1], p_all=ivw$pval[1],
       b_nopav = if (!is.null(primary_np)) primary_np$b[1] else NA,
       p_nopav = if (!is.null(primary_np)) primary_np$pval[1] else NA,
       n_nopav = nrow(dat_np), pp_h4 = unname(cc$summary["PP.H4.abf"]))
}

res_olink <- run_platform(olink_protein, "Olink (UKB-PPP-style)", 54219)
res_soma  <- run_platform(soma_protein,  "SomaScan (deCODE-style)", 35559)

cat("\n-- Cross-platform comparison --\n")
cmp <- data.frame(platform = c(res_olink$label, res_soma$label),
                   n_instr = c(res_olink$n_instr, res_soma$n_instr),
                   b_all = c(res_olink$b_all, res_soma$b_all),
                   p_all = c(res_olink$p_all, res_soma$p_all),
                   b_pav_excluded = c(res_olink$b_nopav, res_soma$b_nopav),
                   p_pav_excluded = c(res_olink$p_nopav, res_soma$p_nopav),
                   pp_h4 = c(res_olink$pp_h4, res_soma$pp_h4))
print(cmp)

dir_agree_all <- sign(res_olink$b_all) == sign(res_soma$b_all)
mag_ratio_all <- max(abs(res_olink$b_all), abs(res_soma$b_all)) / min(abs(res_olink$b_all), abs(res_soma$b_all))
cat("\nAll-instrument direction agreement:", dir_agree_all, " magnitude ratio:", round(mag_ratio_all,2), "\n")
cat("PAV-excluded SomaScan estimate (should move toward Olink once artifact SNP dropped):",
    round(res_soma$b_nopav, 4), "vs all-instrument SomaScan:", round(res_soma$b_all, 4),
    "vs Olink (clean):", round(res_olink$b_all, 4), "\n")
cat("Ground truth planted MR effect:", true_mr_effect, "\n")
