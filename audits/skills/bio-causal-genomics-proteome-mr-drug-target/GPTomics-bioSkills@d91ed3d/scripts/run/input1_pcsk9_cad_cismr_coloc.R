# Input 1 (Canonical): "I have UKB-PPP cis-pQTLs for PCSK9 within +/-500 kb of the gene and
# CARDIoGRAMplusC4D CAD summary stats. Run cis-IVW with weak-IV filtering, harmonise with action=2,
# triangulate with coloc.abf at p12=5e-6, and report PP.H4 plus PAV-excluded sensitivity. Annotate
# every cis-pQTL with VEP first."
#
# SYNTHETIC DATA. No real UKB-PPP or CARDIoGRAMplusC4D data used (no unauthenticated public download
# of individual-record pQTL/CAD summary stats was available inside the audit env). Ground truth is
# planted: one causal SNP (rs_causal) drives both protein level and CAD risk; LD-linked neighbours get
# marginal signal from the causal SNP scaled by an AR(1)-decay LD matrix (standard coloc-style
# simulation). No local plink + 1000G reference bfile is available in this env (checked: no
# genetics.binaRies, no cached 1kg bfile) so ld_clump()/ld_matrix() against a real reference panel is
# NOT executed; the correlated-instrument step below uses the same synthetic LD matrix that generated
# the summary stats (stated explicitly, not presented as a real reference panel).

suppressPackageStartupMessages({
  library(TwoSampleMR)
  library(MendelianRandomization)
  library(coloc)
})

set.seed(20260917)

# ---- 1. Simulate a 60-SNP cis-window around PCSK9 (hg38 chr1:55,039,548-55,064,852; +/-500kb) ----
n_snp <- 60
gene_chr <- 1; gene_start <- 55039548; gene_end <- 55064852; win <- 500000
pos <- sort(sample((gene_start - win):(gene_end + win), n_snp))
causal_idx <- 30L  # planted causal SNP

# AR(1)-decay LD structure by genomic distance (rho decays with distance in bp)
d <- abs(outer(pos, pos, "-"))
ld <- 0.9 ^ (d / 20000)          # correlation decays over ~20kb scale
diag(ld) <- 1

maf <- runif(n_snp, 0.05, 0.45)
snp_id <- sprintf("rs%07d", 1000000 + seq_len(n_snp))

# True per-allele causal effect on protein level (standardized), 0 everywhere except causal_idx
true_beta_protein <- rep(0, n_snp)
true_beta_protein[causal_idx] <- 0.35   # SD units of protein level per effect allele

# Marginal (LD-tagged) true effect on protein = LD-weighted causal effect
marg_beta_protein <- as.numeric(ld[, causal_idx]) * true_beta_protein[causal_idx]

# Protein GWAS (quantitative, N=54219, matches UKB-PPP Sun 2023 Olink N)
n_protein <- 54219
se_protein <- sqrt(1 / (2 * maf * (1 - maf) * n_protein)) * 3.2  # scaled se, realistic order of magnitude
beta_protein <- marg_beta_protein + rnorm(n_snp, 0, se_protein)
p_protein <- 2 * pnorm(-abs(beta_protein / se_protein))

# CAD outcome: causal SNP acts on CAD ONLY through the protein (true cis-MR causal OR)
true_mr_effect <- 0.45   # log-OR per SD protein (drives CAD via PCSK9 lowering-like mechanism)
n_cad <- 122733; case_frac <- 0.34
marg_beta_cad <- marg_beta_protein * true_mr_effect
se_cad <- sqrt(1 / (2 * maf * (1 - maf) * n_cad * case_frac * (1 - case_frac))) * 1.1
beta_cad <- marg_beta_cad + rnorm(n_snp, 0, se_cad)
p_cad <- 2 * pnorm(-abs(beta_cad / se_cad))

a1 <- sample(c("A", "C", "G", "T"), n_snp, replace = TRUE)
a2 <- sapply(a1, function(x) sample(setdiff(c("A", "C", "G", "T"), x), 1))

pqtl_full <- data.frame(SNP = snp_id, CHR = gene_chr, POS = pos, BETA = beta_protein,
                         SE = se_protein, A1 = a1, A2 = a2, EAF = maf, P = p_protein,
                         stringsAsFactors = FALSE)
cad_full <- data.frame(SNP = snp_id, CHR = gene_chr, POS = pos, BETA = beta_cad,
                        SE = se_cad, A1 = a1, A2 = a2, EAF = maf, P = p_cad,
                        stringsAsFactors = FALSE)

write.table(pqtl_full, "../data/synth_pcsk9_ukbppp_full_window.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
write.table(cad_full, "../data/synth_cad_gwas_pcsk9_window.tsv", sep = "\t", row.names = FALSE, quote = FALSE)

# Synthetic VEP PAV annotation: mark two SNPs near the causal one as missense (PAV) to exercise the
# PAV-excluded sensitivity panel the SKILL.md requires.
pav_snps <- snp_id[c(causal_idx, causal_idx + 1)]
vep <- data.frame(SNP = pav_snps, Consequence = c("missense_variant", "synonymous_variant"))
write.table(vep, "../data/synth_pcsk9_vep_pav.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
cat("Planted causal SNP:", snp_id[causal_idx], " (also flagged PAV=missense in synthetic VEP)\n")

# ---- 2. Filter to genome-wide-significant cis-SNPs, F-statistic floor (Skill's documented steps) ----
pqtl_sig <- subset(pqtl_full, P < 5e-8)
pqtl_sig$f_stat <- (pqtl_sig$BETA / pqtl_sig$SE)^2
pqtl_sig <- subset(pqtl_sig, f_stat >= 10)
cat("Cis-pQTLs after P<5e-8 + F>=10 filter:", nrow(pqtl_sig), "\n")

pav_consequences <- c("missense_variant", "stop_gained", "stop_lost", "frameshift_variant",
                       "splice_acceptor_variant", "splice_donor_variant", "start_lost",
                       "protein_altering_variant")
pqtl_sig$is_pav <- pqtl_sig$SNP %in% vep$SNP[vep$Consequence %in% pav_consequences]
cat("PAV-flagged among significant cis-pQTLs:", sum(pqtl_sig$is_pav), "\n")

# NOTE on clumping: no local plink+1000G bfile is present in this env (verified: genetics.binaRies not
# installed, no cached reference panel). ld_clump() is NOT executed here. Since the synthetic window
# already has only a handful of genome-wide-significant SNPs (F>=10 selects mainly near the causal
# locus, where LD is highest), skipping clumping in this synthetic case is flagged, not silently
# assumed equivalent to a real clumping step.
exposure_dat <- format_data(pqtl_sig, type = "exposure",
    snp_col = "SNP", beta_col = "BETA", se_col = "SE",
    effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P")

outcome_dat <- format_data(cad_full[cad_full$SNP %in% exposure_dat$SNP, ], type = "outcome",
    snp_col = "SNP", beta_col = "BETA", se_col = "SE",
    effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P")

dat <- harmonise_data(exposure_dat, outcome_dat, action = 2)
cat("Harmonised instruments:", nrow(dat), "/", nrow(exposure_dat), "\n")

run_cis_panel <- function(d) {
  methods <- if (nrow(d) == 1) "mr_wald_ratio" else
             if (nrow(d) >= 10) c("mr_ivw", "mr_egger_regression", "mr_weighted_median") else
             c("mr_ivw", "mr_weighted_median")
  mr(d, method_list = methods)
}

primary <- run_cis_panel(dat)
cat("\n-- Primary cis-MR panel --\n"); print(primary[, c("method","nsnp","b","se","pval")])

dat$is_pav <- dat$SNP %in% vep$SNP[vep$Consequence %in% pav_consequences]
dat_no_pav <- subset(dat, !is_pav)
cat("\nInstruments after PAV exclusion:", nrow(dat_no_pav), "\n")
pav_excluded <- if (nrow(dat_no_pav) >= 1) run_cis_panel(dat_no_pav) else NULL
if (!is.null(pav_excluded)) { cat("-- PAV-excluded panel --\n"); print(pav_excluded[, c("method","nsnp","b","se","pval")]) }

# ---- 3. Correlated-instrument cis-IVW using the SAME synthetic LD matrix that generated the data ----
if (nrow(dat) >= 2) {
  idx_common <- match(dat$SNP, snp_id)
  ld_sub <- ld[idx_common, idx_common]
  mr_obj <- mr_input(bx = dat$beta.exposure, bxse = dat$se.exposure,
                      by = dat$beta.outcome, byse = dat$se.outcome,
                      correlation = ld_sub)
  result_correl <- mr_ivw(mr_obj, model = "default", correl = TRUE)
  cat("\n-- Cis-IVW with correl=TRUE (synthetic in-window LD) --\n")
  cat("Estimate:", result_correl@Estimate, " SE:", result_correl@StdError,
      " CI:[", result_correl@CILower, ",", result_correl@CIUpper, "]\n")
}

# ---- 4. Colocalization on the full window (not just significant SNPs) ----
coloc_res <- coloc.abf(
  dataset1 = list(beta = pqtl_full$BETA, varbeta = pqtl_full$SE^2, snp = pqtl_full$SNP,
                   type = "quant", N = n_protein, sdY = 1),
  dataset2 = list(beta = cad_full$BETA, varbeta = cad_full$SE^2, snp = cad_full$SNP,
                   type = "cc", N = n_cad, s = case_frac),
  p1 = 1e-4, p2 = 1e-4, p12 = 5e-6)

cat("\n-- coloc.abf (full 60-SNP window) --\n")
print(coloc_res$summary)

decision <- list(
  cis_mr_p = primary$pval[primary$method == "Inverse variance weighted"][1],
  cis_mr_beta = primary$b[primary$method == "Inverse variance weighted"][1],
  coloc_pp_h4 = unname(coloc_res$summary["PP.H4.abf"]),
  n_instruments = nrow(dat),
  n_after_pav_exclusion = nrow(dat_no_pav),
  pav_excluded_p = if (!is.null(pav_excluded)) pav_excluded$pval[pav_excluded$method=="Inverse variance weighted"][1] else NA,
  bonferroni_2923 = 0.05 / 2923,
  triangulation_passed = !is.null(pav_excluded) &&
                          !is.na(primary$pval[primary$method == "Inverse variance weighted"][1]) &&
                          primary$pval[primary$method == "Inverse variance weighted"][1] < 0.05 / 2923 &&
                          unname(coloc_res$summary["PP.H4.abf"]) >= 0.8
)
cat("\n-- Decision summary --\n")
str(decision)
cat("\nGround truth: planted cis-MR log-effect =", true_mr_effect, "; recovered IVW b =",
    round(decision$cis_mr_beta, 4), "\n")
