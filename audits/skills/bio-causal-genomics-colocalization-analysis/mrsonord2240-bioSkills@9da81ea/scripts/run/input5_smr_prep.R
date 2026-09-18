# Input 5 -- Stress: independent regression test of the SMR + HEIDI recipe
# (P1 fix: fix log claims a real SMR 1.3.1 run recovering planted truth for both
#  a shared-causal and a linkage/distinct-causal-in-LD scenario. This re-derives
#  fresh synthetic data, independent seed/params from the fixer's own tmp_smr_test/,
#  and writes the plink ped/map + .ma + .esd/.flist inputs the SMR CLI needs.)
#
# Two scenarios written side by side, sharing the same genotype matrix + GWAS:
#   scenario "shared":  eQTL causal SNP == GWAS causal SNP           -> expect SMR sig, HEIDI non-reject (p>0.05)
#   scenario "linkage": eQTL causal SNP is a DIFFERENT SNP in LD with the GWAS causal SNP -> expect HEIDI reject (p<=0.05)

set.seed(20260918)
n_ind  <- 2500
n_snps <- 50
mafs   <- runif(n_snps, 0.15, 0.45)

# --- Simulate genotypes with AR(1)-like LD via a liability-threshold model ---
rho <- 0.80
Sigma <- rho^abs(outer(1:n_snps, 1:n_snps, '-'))
Lchol <- chol(Sigma)

make_haplotype <- function() {
  Z <- matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% Lchol
  H <- matrix(0L, n_ind, n_snps)
  for (j in 1:n_snps) {
    thresh <- qnorm(1 - mafs[j])
    H[, j] <- as.integer(Z[, j] > thresh)
  }
  H
}
hap1 <- make_haplotype()
hap2 <- make_haplotype()
G <- hap1 + hap2   # 0/1/2 dosage genotype matrix, n_ind x n_snps

chr <- 1
bp  <- seq(1000000, by = 20000, length.out = n_snps)
snp_ids <- paste0('rs', 9000 + 1:n_snps)
a1 <- rep('A', n_snps); a2 <- rep('G', n_snps)

# LD sanity check: r2 between adjacent-ish SNPs
r_check <- cor(G[, 20], G[, 22])
cat(sprintf('Sanity: r(G[,20],G[,22]) = %.3f (AR1 rho=0.80 should give moderate-high LD nearby)\n', r_check))

causal_gwas <- 25          # GWAS causal SNP index (shared scenario truth)
causal_eqtl_linkage <- 27  # distinct eQTL causal SNP, in LD with causal_gwas, for the linkage scenario
cat(sprintf('PLANTED TRUTH: GWAS causal = %s (idx %d); shared-scenario eQTL causal = same SNP; linkage-scenario eQTL causal = %s (idx %d), r2(causal_gwas,causal_eqtl_linkage)=%.3f\n',
            snp_ids[causal_gwas], causal_gwas, snp_ids[causal_eqtl_linkage], causal_eqtl_linkage,
            cor(G[, causal_gwas], G[, causal_eqtl_linkage])^2))

# --- GWAS phenotype (continuous, one causal SNP) ---
y_gwas <- 0.35 * scale(G[, causal_gwas]) + rnorm(n_ind, 0, 1)

get_sumstats <- function(y, G) {
  beta <- se <- pval <- freq <- numeric(ncol(G))
  for (j in 1:ncol(G)) {
    fit <- summary(lm(y ~ G[, j]))$coefficients
    beta[j] <- fit[2, 1]; se[j] <- fit[2, 2]; pval[j] <- fit[2, 4]
    freq[j] <- mean(G[, j]) / 2
  }
  data.frame(SNP = snp_ids, A1 = a1, A2 = a2, freq = freq, b = beta, se = se, p = pval, N = nrow(G))
}
gwas_ss <- get_sumstats(as.vector(y_gwas), G)
write.table(gwas_ss, 'smr_test/gwas.ma', quote = FALSE, row.names = FALSE, sep = '\t')
cat(sprintf('GWAS top SNP: %s p=%.3e (planted causal %s)\n',
            gwas_ss$SNP[which.min(gwas_ss$p)], min(gwas_ss$p), snp_ids[causal_gwas]))

# --- eQTL phenotypes: shared-causal scenario and linkage scenario ---
y_eqtl_shared  <- 0.50 * scale(G[, causal_gwas])          + rnorm(n_ind, 0, 1)
y_eqtl_linkage <- 0.50 * scale(G[, causal_eqtl_linkage])  + rnorm(n_ind, 0, 1)

write_esd <- function(y, tag) {
  ss <- get_sumstats(as.vector(y), G)
  esd <- data.frame(Chr = chr, SNP = ss$SNP, Bp = bp, A1 = ss$A1, A2 = ss$A2,
                     Freq = ss$freq, Beta = ss$b, se = ss$se, p = ss$p)
  fn <- sprintf('smr_test/eqtl_%s.esd', tag)
  write.table(esd, fn, quote = FALSE, row.names = FALSE, sep = '\t')
  cat(sprintf('[%s] eQTL top SNP: %s p=%.3e\n', tag, ss$SNP[which.min(ss$p)], min(ss$p)))
  fn
}
dir.create('smr_test', showWarnings = FALSE)
# re-run write_esd now that dir exists (data.frame writes above happened before dir existed for gwas.ma -- fix order)
write.table(gwas_ss, 'smr_test/gwas.ma', quote = FALSE, row.names = FALSE, sep = '\t')
esd_shared  <- write_esd(y_eqtl_shared,  'shared')
esd_linkage <- write_esd(y_eqtl_linkage, 'linkage')

# --- .flist files (SMR eqtl-flist format: Chr ProbeID GeneticDistance ProbeBp Gene Orientation PathOfEsd) ---
write_flist <- function(esd_path, tag) {
  fl <- data.frame(Chr = chr, ProbeID = paste0('probe_', tag), GeneticDistance = 0,
                    ProbeBp = bp[causal_gwas], Gene = paste0('gene_', tag), Orientation = '+',
                    PathOfEsd = normalizePath(esd_path, winslash = '/', mustWork = FALSE))
  fn <- sprintf('smr_test/eqtl_%s.flist', tag)
  write.table(fl, fn, quote = FALSE, row.names = FALSE, sep = '\t')
  fn
}
write_flist(esd_shared, 'shared')
write_flist(esd_linkage, 'linkage')

# --- PLINK .ped / .map for the shared genotype/LD reference ---
map_df <- data.frame(chr = chr, snp = snp_ids, cm = 0, bp = bp)
write.table(map_df, 'smr_test/ref.map', quote = FALSE, row.names = FALSE, col.names = FALSE, sep = '\t')

ped_alleles <- matrix('', n_ind, 2 * n_snps)
allele_letters <- c('A', 'G')
for (j in 1:n_snps) {
  # genotype dosage 0/1/2 -> two allele columns using A1/A2 (A=effect, G=other)
  g <- G[, j]
  a1_count <- g          # number of A1(A) alleles
  col1 <- ifelse(a1_count >= 1, 'A', 'G')
  col2 <- ifelse(a1_count == 2, 'A', ifelse(a1_count == 1, 'A', 'G'))
  # simpler explicit mapping: 0 -> G G ; 1 -> A G ; 2 -> A A
  col1 <- ifelse(g == 0, 'G', 'A')
  col2 <- ifelse(g == 2, 'A', 'G')
  ped_alleles[, 2 * j - 1] <- col1
  ped_alleles[, 2 * j]     <- col2
}
fam_ids <- paste0('IND', 1:n_ind)
ped_df <- cbind(fam_ids, fam_ids, 0, 0, 0, -9, ped_alleles)
write.table(ped_df, 'smr_test/ref.ped', quote = FALSE, row.names = FALSE, col.names = FALSE, sep = ' ')

cat('\nFiles written to smr_test/: gwas.ma, eqtl_shared.esd/.flist, eqtl_linkage.esd/.flist, ref.ped/.map\n')
