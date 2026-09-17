# Simulate a pair of GWAS summary-statistics files consistent EXACTLY with the
# bivariate LDSC generative model, for a given planted h2_1, h2_2, rg and sample
# overlap. Used by input1/input2/input3 scripts. Synthetic data -- not real GWAS.
#
# Model (matches SKILL.md's own equation):
#   E[Z1_j Z2_j] = sqrt(N1*N2) * rg * sqrt(h2_1*h2_2) / M * L2_j + rho_overlap
#   E[Z_j^2]     = 1 + N * h2 * L2_j / M
# Each block b (size s_b, L2_j = s_b for its member SNPs) carries one latent
# causal-effect pair (beta1_b, beta2_b) with
#   Var(beta1_b) = h2_1 * s_b / M,  Var(beta2_b) = h2_2 * s_b / M,
#   Cov(beta1_b, beta2_b) = rg * sqrt(h2_1*h2_2) * s_b / M
# All s_b tag SNPs in the block inherit the block's true effect (perfect LD),
# then per-SNP sampling noise (and correlated noise under sample overlap) is added.

simulate_gwas_pair <- function(ld_dir, N1, N2, h2_1, h2_2, rg,
                                overlap_n = 0, overlap_rho = 0,
                                out_prefix, seed) {
  set.seed(seed)
  ld <- readRDS(file.path(ld_dir, "block_structure.rds"))
  block_id <- ld$block_id; block_sizes <- ld$block_sizes; L2 <- ld$L2
  snp_id <- ld$snp_id; M <- ld$M_total
  K <- length(block_sizes)

  var1 <- h2_1 * block_sizes / M
  var2 <- h2_2 * block_sizes / M
  covb <- rg * sqrt(h2_1 * h2_2) * block_sizes / M

  beta1_block <- numeric(K); beta2_block <- numeric(K)
  for (b in seq_len(K)) {
    Sigma <- matrix(c(var1[b], covb[b], covb[b], var2[b]), 2, 2)
    Sigma <- Sigma + diag(1e-12, 2)  # numerical guard for size-0 edge case
    ch <- tryCatch(chol(Sigma), error = function(e) NULL)
    z <- rnorm(2)
    if (is.null(ch)) {
      beta1_block[b] <- sqrt(var1[b]) * z[1]
      beta2_block[b] <- rg * sqrt(var2[b]) * z[1] + sqrt(max(var2[b] * (1 - rg^2), 0)) * z[2]
    } else {
      bb <- z %*% ch
      beta1_block[b] <- bb[1]; beta2_block[b] <- bb[2]
    }
  }
  beta1_snp <- beta1_block[block_id]
  beta2_snp <- beta2_block[block_id]

  # sampling noise, correlated under sample overlap (Ns shared individuals,
  # phenotypic correlation overlap_rho among them): corr(eps1,eps2) = overlap_rho *
  # overlap_n / sqrt(N1*N2)
  rho_eps <- overlap_rho * overlap_n / sqrt(N1 * N2)
  rho_eps <- max(min(rho_eps, 0.98), -0.98)
  eps <- matrix(rnorm(2 * M), ncol = 2)
  L <- chol(matrix(c(1, rho_eps, rho_eps, 1), 2, 2))
  eps <- eps %*% L

  z1 <- beta1_snp * sqrt(N1) + eps[, 1]
  z2 <- beta2_snp * sqrt(N2) + eps[, 2]

  df1 <- data.frame(SNP = snp_id, A1 = "A", A2 = "G", N = N1, Z = z1)
  df2 <- data.frame(SNP = snp_id, A1 = "A", A2 = "G", N = N2, Z = z2)

  f1 <- paste0(out_prefix, "_trait1.sumstats.gz")
  f2 <- paste0(out_prefix, "_trait2.sumstats.gz")
  g1 <- gzfile(f1, "wt"); write.table(df1, g1, sep = "\t", quote = FALSE, row.names = FALSE); close(g1)
  g2 <- gzfile(f2, "wt"); write.table(df2, g2, sep = "\t", quote = FALSE, row.names = FALSE); close(g2)

  list(file1 = f1, file2 = f2,
       truth = list(h2_1 = h2_1, h2_2 = h2_2, rg = rg, N1 = N1, N2 = N2,
                    overlap_n = overlap_n, overlap_rho = overlap_rho,
                    expected_intercept = rho_eps,
                    mean_chisq1 = mean(z1^2), mean_chisq2 = mean(z2^2)))
}
