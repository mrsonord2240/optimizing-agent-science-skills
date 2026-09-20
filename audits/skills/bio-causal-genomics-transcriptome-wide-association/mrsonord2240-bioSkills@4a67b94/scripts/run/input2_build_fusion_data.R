# Synthetic-data builder for Input 2 (FUSION TWAS + conditional analysis).
# All data below is SYNTHETIC except the genotype/LD reference, which is the real
# small test panel bundled with plink2R (957 individuals x 14389 chr1 SNPs,
# tools/src/plink2R/data.bed/.bim/.fam) -- real genotypes, used here purely as an
# LD reference, not tied to any real phenotype.
#
# Plants a true signal at GENE1 (weight concentrated on one real SNP, GWAS Z=6.5
# at that SNP) and a null gene GENE2 (weight on a different real SNP, GWAS Z~N(0,1)
# at that SNP). All other SNPs in the reference get GWAS Z~N(0,1) noise.
# Expectation: FUSION.assoc_test.R reports |TWAS.Z| ~ 6.5 for GENE1 and a small
# |TWAS.Z| for GENE2 (consistent with noise), letting us assert directly against a
# known planted answer rather than merely checking the script exits 0.

set.seed(20260917)

base    <- "F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association"
srcdir  <- "F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/src/plink2R"
lddir   <- file.path(base, "data/fusion/ld")
wgtdir  <- file.path(base, "data/fusion/wgt")

# 1. Copy the real bundled genotype panel into an LD reference named chr1 (FUSION
#    appends the --chr value directly to --ref_ld_chr, so the prefix must end in "1").
file.copy(file.path(srcdir, "data.bed"), file.path(lddir, "EUR.1.bed"), overwrite = TRUE)
file.copy(file.path(srcdir, "data.bim"), file.path(lddir, "EUR.1.bim"), overwrite = TRUE)
file.copy(file.path(srcdir, "data.fam"), file.path(lddir, "EUR.1.fam"), overwrite = TRUE)

bim <- read.table(file.path(srcdir, "data.bim"), header = FALSE, as.is = TRUE,
                   col.names = c("CHR","SNP","CM","POS","A1","A2"))

# 2. Pick two real, unrelated SNPs from the panel to anchor GENE1 (true) and GENE2 (null).
snp1 <- bim[500, ]   # GENE1's single-SNP ("top1") model weight
snp2 <- bim[7500, ]  # GENE2's single-SNP ("top1") model weight (non-palindromic: G/A)
stopifnot(snp1$SNP != snp2$SNP)

# 3. Build per-gene weight RDat files in the exact structure FUSION.assoc_test.R expects:
#    wgt.matrix (SNP x model, rownames = SNP ids), snps (bim-format df), cv.performance
#    (rows containing "rsq"/"pval", columns = model names), hsq (heritability estimate).
write_wgt <- function(snp_row, path, rsq, pval, hsq_val) {
  wgt.matrix <- matrix(1, nrow = 1, ncol = 1, dimnames = list(snp_row$SNP, "top1"))
  snps <- data.frame(V1 = snp_row$CHR, V2 = snp_row$SNP, V3 = 0, V4 = snp_row$POS,
                      V5 = snp_row$A1, V6 = snp_row$A2, stringsAsFactors = FALSE)
  cv.performance <- matrix(c(rsq, pval), nrow = 2, ncol = 1,
                            dimnames = list(c("rsq","pval"), "top1"))
  hsq <- c(hsq_val, 0.001)
  save(wgt.matrix, snps, cv.performance, hsq, file = path)
}

write_wgt(snp1, file.path(wgtdir, "GENE1.wgt.RDat"), rsq = 0.18, pval = 1e-6, hsq_val = 0.15)
write_wgt(snp2, file.path(wgtdir, "GENE2.wgt.RDat"), rsq = 0.09, pval = 1e-3, hsq_val = 0.06)

# 4. weights.pos: WGT, ID, CHR, P0, P1 columns (as required by FUSION.assoc_test.R --weights).
pos <- data.frame(
  PANEL = "SYNTH_PANEL",
  WGT   = c("GENE1.wgt.RDat", "GENE2.wgt.RDat"),
  ID    = c("GENE1", "GENE2"),
  CHR   = c(1, 1),
  P0    = c(snp1$POS - 5e5, snp2$POS - 5e5),
  P1    = c(snp1$POS + 5e5, snp2$POS + 5e5),
  N     = c(838, 838)
)
write.table(pos, file.path(base, "data/fusion/weights.pos"), quote = FALSE, row.names = FALSE, sep = "\t")

# 5. Synthetic GWAS sumstats over every SNP in the LD reference: SNP A1 A2 Z, BETA, SE
#    Null Z ~ N(0,1) everywhere except the two planted-effect SNPs.
z <- rnorm(nrow(bim), 0, 1)
z[bim$SNP == snp1$SNP] <- 6.5   # planted true signal (GENE1)
z[bim$SNP == snp2$SNP] <- rnorm(1, 0, 1)  # GENE2 stays null
gwas <- data.frame(SNP = bim$SNP, A1 = bim$A1, A2 = bim$A2, Z = z,
                    BETA = z * 0.05, SE = 0.05, N = 838)
write.table(gwas, file.path(base, "data/fusion/gwas.sumstats"), quote = FALSE, row.names = FALSE, sep = "\t")

cat("Planted GENE1 top SNP:", snp1$SNP, "at POS", snp1$POS, "GWAS Z =", z[bim$SNP == snp1$SNP], "\n")
cat("Null    GENE2 top SNP:", snp2$SNP, "at POS", snp2$POS, "GWAS Z =", z[bim$SNP == snp2$SNP], "\n")
cat("Wrote:", file.path(base, "data/fusion/weights.pos"), "\n")
cat("Wrote:", file.path(base, "data/fusion/gwas.sumstats"), "\n")
cat("Wrote:", wgtdir, "/GENE1.wgt.RDat ,", wgtdir, "/GENE2.wgt.RDat\n")
cat("Wrote LD reference:", lddir, "/EUR.1.[bed|bim|fam] (REAL genotypes, plink2R bundled test panel, used only as LD ref)\n")
