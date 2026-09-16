# ============================================================================
# SYNTHETIC DATA GENERATOR -- audit of bio-experimental-design-sample-size
# Every file this writes is SYNTHETIC. No real biological sample is involved.
# Ground truth is PLANTED so that a sample-size recommendation can be checked
# against the power that is actually achieved.
# ============================================================================
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
set.seed(20260916)
outdir <- "F:/OpenScience/audits/bio-experimental-design-sample-size/data"

nGenes   <- 12000
TRUE_DISP <- 0.35          # planted NB dispersion (human tumour/normal-like, > the 0.2 guess)
TRUE_PI0  <- 0.95          # 5% of genes truly DE
TRUE_FC   <- 1.5           # planted fold change for the DE genes (half up, half down)
BASE_MU   <- 40            # planted mean count for a library of ~ nGenes*BASE_MU reads

de_idx  <- sort(sample.int(nGenes, round(nGenes * (1 - TRUE_PI0))))
up      <- rep(FALSE, nGenes); up[sample(de_idx, length(de_idx) %/% 2)] <- TRUE
fc_vec  <- rep(1, nGenes); fc_vec[de_idx] <- ifelse(up[de_idx], TRUE_FC, 1 / TRUE_FC)
# gene-level mean heterogeneity, so the dispersion-mean trend is not degenerate
mu_vec  <- BASE_MU * exp(rnorm(nGenes, 0, 0.8))

sim_counts <- function(n_per_group, mu_scale = 1) {
  m <- matrix(0L, nGenes, 2 * n_per_group)
  for (j in seq_len(n_per_group))
    m[, j] <- rnbinom(nGenes, mu = mu_vec * mu_scale, size = 1 / TRUE_DISP)
  for (j in seq_len(n_per_group))
    m[, n_per_group + j] <- rnbinom(nGenes, mu = mu_vec * fc_vec * mu_scale, size = 1 / TRUE_DISP)
  rownames(m) <- sprintf("GENE%05d", seq_len(nGenes))
  colnames(m) <- c(sprintf("CTRL_%02d", seq_len(n_per_group)),
                   sprintf("TUMR_%02d", seq_len(n_per_group)))
  m
}

# --- Pilot A: the under-sized pilot a researcher usually actually has (2 vs 2) ----
pilotA <- sim_counts(2)
write.csv(pilotA, file.path(outdir, "SYNTHETIC_pilot_2v2_counts.csv"), quote = FALSE)
write.csv(data.frame(sample = colnames(pilotA),
                     condition = rep(c("control", "tumor"), each = 2)),
          file.path(outdir, "SYNTHETIC_pilot_2v2_coldata.csv"), row.names = FALSE, quote = FALSE)

# --- Pilot B: a generous pilot (6 vs 6), same generative truth -------------------
pilotB <- sim_counts(6)
write.csv(pilotB, file.path(outdir, "SYNTHETIC_pilot_6v6_counts.csv"), quote = FALSE)
write.csv(data.frame(sample = colnames(pilotB),
                     condition = rep(c("control", "tumor"), each = 6)),
          file.path(outdir, "SYNTHETIC_pilot_6v6_coldata.csv"), row.names = FALSE, quote = FALSE)

# --- Ground-truth manifest -------------------------------------------------------
truth <- data.frame(gene = sprintf("GENE%05d", seq_len(nGenes)),
                    mu_control = mu_vec, fold_change = fc_vec,
                    is_de = seq_len(nGenes) %in% de_idx, dispersion = TRUE_DISP)
write.csv(truth, file.path(outdir, "SYNTHETIC_ground_truth.csv"), row.names = FALSE, quote = FALSE)

cat("SYNTHETIC data written to", outdir, "\n")
cat(sprintf("  nGenes=%d  true dispersion=%.2f  pi0=%.2f  true FC=%.1f  base mu=%d\n",
            nGenes, TRUE_DISP, TRUE_PI0, TRUE_FC, BASE_MU))
cat(sprintf("  truly DE genes: %d (%d up, %d down)\n", length(de_idx), sum(up), length(de_idx)-sum(up)))
cat(sprintf("  pilot 2v2 dims: %s   pilot 6v6 dims: %s\n",
            paste(dim(pilotA), collapse="x"), paste(dim(pilotB), collapse="x")))
