# Fresh synthetic-data builder for the re-audit's FUSION single-SNP crash reproduction.
# Deliberately uses different SNP indices and a different seed than the fixer's own
# audit fixture (input2_build_fusion_data.R used snp1=bim[500,], snp2=bim[7500,], seed 20260917)
# so this is genuinely independent verification, not a re-run of the same file.
#
# Real genotypes (plink2R bundled test panel, 957 indiv x 14389 chr1 SNPs) used only as an
# LD reference, no real phenotype attached. Three genes this time: GENE_TRUE (single-SNP
# "top1" model, true planted signal), GENE_NULL (single-SNP "top1" model, null), and
# GENE_MULTI (2-SNP model, to confirm the drop=FALSE patch doesn't break the >1-SNP path).

set.seed(9182026)

base    <- "C:/Users/User/AppData/Local/Temp/claude/f--optimizing-agent-science-skills/a17db7c0-9e8e-4d1d-8394-29c143f93c09/scratchpad/twas-reaudit"
srcdir  <- "F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/src/plink2R"
lddir   <- file.path(base, "data/fusion/ld")
wgtdir  <- file.path(base, "data/fusion/wgt")

file.copy(file.path(srcdir, "data.bed"), file.path(lddir, "EUR.1.bed"), overwrite = TRUE)
file.copy(file.path(srcdir, "data.bim"), file.path(lddir, "EUR.1.bim"), overwrite = TRUE)
file.copy(file.path(srcdir, "data.fam"), file.path(lddir, "EUR.1.fam"), overwrite = TRUE)

bim <- read.table(file.path(srcdir, "data.bim"), header = FALSE, as.is = TRUE,
                   col.names = c("CHR","SNP","CM","POS","A1","A2"))

snp_true <- bim[300, ]
snp_null <- bim[900, ]
snp_multi_a <- bim[950, ]
snp_multi_b <- bim[951, ]
stopifnot(snp_true$CHR == 1, snp_null$CHR == 1, snp_multi_a$CHR == 1, snp_multi_b$CHR == 1)
stopifnot(length(unique(c(snp_true$SNP, snp_null$SNP, snp_multi_a$SNP, snp_multi_b$SNP))) == 4)

write_wgt_single <- function(snp_row, path, rsq, pval, hsq_val) {
  wgt.matrix <- matrix(1, nrow = 1, ncol = 1, dimnames = list(snp_row$SNP, "top1"))
  snps <- data.frame(V1 = snp_row$CHR, V2 = snp_row$SNP, V3 = 0, V4 = snp_row$POS,
                      V5 = snp_row$A1, V6 = snp_row$A2, stringsAsFactors = FALSE)
  cv.performance <- matrix(c(rsq, pval), nrow = 2, ncol = 1,
                            dimnames = list(c("rsq","pval"), "top1"))
  hsq <- c(hsq_val, 0.001)
  save(wgt.matrix, snps, cv.performance, hsq, file = path)
}

write_wgt_multi <- function(snp_rows, weights, path, rsq, pval, hsq_val) {
  wgt.matrix <- matrix(weights, nrow = length(weights), ncol = 1,
                        dimnames = list(snp_rows$SNP, "top1"))
  snps <- data.frame(V1 = snp_rows$CHR, V2 = snp_rows$SNP, V3 = 0, V4 = snp_rows$POS,
                      V5 = snp_rows$A1, V6 = snp_rows$A2, stringsAsFactors = FALSE)
  cv.performance <- matrix(c(rsq, pval), nrow = 2, ncol = 1,
                            dimnames = list(c("rsq","pval"), "top1"))
  hsq <- c(hsq_val, 0.001)
  save(wgt.matrix, snps, cv.performance, hsq, file = path)
}

write_wgt_single(snp_true, file.path(wgtdir, "GENE_TRUE.wgt.RDat"), rsq = 0.20, pval = 1e-7, hsq_val = 0.18)
write_wgt_single(snp_null, file.path(wgtdir, "GENE_NULL.wgt.RDat"), rsq = 0.08, pval = 1e-2, hsq_val = 0.05)
multi_rows <- rbind(snp_multi_a, snp_multi_b)
write_wgt_multi(multi_rows, c(0.6, 0.4), file.path(wgtdir, "GENE_MULTI.wgt.RDat"), rsq = 0.12, pval = 1e-4, hsq_val = 0.10)

pos <- data.frame(
  PANEL = "REAUDIT_PANEL",
  WGT   = c("GENE_TRUE.wgt.RDat", "GENE_NULL.wgt.RDat", "GENE_MULTI.wgt.RDat"),
  ID    = c("GENE_TRUE", "GENE_NULL", "GENE_MULTI"),
  CHR   = c(1, 1, 1),
  P0    = c(snp_true$POS - 5e5, snp_null$POS - 5e5, min(multi_rows$POS) - 5e5),
  P1    = c(snp_true$POS + 5e5, snp_null$POS + 5e5, max(multi_rows$POS) + 5e5),
  N     = c(838, 838, 838)
)
write.table(pos, file.path(base, "data/fusion/weights.pos"), quote = FALSE, row.names = FALSE, sep = "\t")

z <- rnorm(nrow(bim), 0, 1)
z[bim$SNP == snp_true$SNP] <- 7.2   # planted true signal, different magnitude than fixer's 6.5
z[bim$SNP == snp_null$SNP] <- rnorm(1, 0, 1)
# multi-SNP gene: no strong planted signal at either SNP (keep both near-null so this is
# purely a "does drop=FALSE break the >1-SNP path" check, not a power check)
z[bim$SNP == snp_multi_a$SNP] <- rnorm(1, 0, 1)
z[bim$SNP == snp_multi_b$SNP] <- rnorm(1, 0, 1)
gwas <- data.frame(SNP = bim$SNP, A1 = bim$A1, A2 = bim$A2, Z = z,
                    BETA = z * 0.05, SE = 0.05, N = 838)
write.table(gwas, file.path(base, "data/fusion/gwas.sumstats"), quote = FALSE, row.names = FALSE, sep = "\t")

cat("Planted GENE_TRUE top SNP:", snp_true$SNP, "at POS", snp_true$POS, "GWAS Z =", z[bim$SNP == snp_true$SNP], "\n")
cat("Null    GENE_NULL top SNP:", snp_null$SNP, "at POS", snp_null$POS, "GWAS Z =", z[bim$SNP == snp_null$SNP], "\n")
cat("Multi   GENE_MULTI SNPs:", snp_multi_a$SNP, snp_multi_b$SNP, "\n")
