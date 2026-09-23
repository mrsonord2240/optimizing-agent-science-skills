# Synthetic lipidomics dataset with planted ground truth for auditing
# bio-metabolomics-lipidomics. NOT real data. Two groups (Control/Disease),
# n=6 each. Includes SPLASH-style deuterated internal standards for PC and
# PE (recognized by lipidr's istd regex) but deliberately NO internal
# standard for the TG class, to test the skill's "one IS per class,
# non-negotiable" claim against a class that lacks one.
set.seed(42)

samples <- c(paste0("Ctrl_", 1:6), paste0("Dis_", 1:6))
group <- rep(c("Control", "Disease"), each = 6)

# Molecule, class, baseline mean (log-normal), fold-change in Disease vs Control
species <- data.frame(
  Molecule = c(
    "PC 34:1", "PC 36:2", "PC 32:0", "PC 16:0/18:1",
    "15:0-18:1(d7) PC",
    "PE 36:2", "PE 34:1",
    "15:0-18:1(d7) PE",
    "TG 52:3", "TG 54:4",
    "Cer 18:1;O2/16:0",
    "LPC 16:0"
  ),
  base_mean = c(
    2.0e6, 1.5e6, 1.8e6, 2.0e6,
    5.0e5,
    1.2e6, 1.4e6,
    5.0e5,
    3.0e6, 2.5e6,
    8.0e5,
    3.0e5
  ),
  fc_disease = c(
    2.0, 1.8, 1.0, 1.0,
    1.0,
    0.5, 1.0,
    1.0,
    1.7, 1.0,
    1.0,
    1.0
  ),
  stringsAsFactors = FALSE
)

cv <- 0.15  # ~15% biological + technical CV, log-normal noise
mat <- matrix(NA_real_, nrow = nrow(species), ncol = length(samples),
              dimnames = list(species$Molecule, samples))

for (i in seq_len(nrow(species))) {
  mu <- log(species$base_mean[i])
  sdlog <- sqrt(log(1 + cv^2))
  ctrl_vals <- rlnorm(6, meanlog = mu, sdlog = sdlog)
  dis_vals  <- rlnorm(6, meanlog = mu + log(species$fc_disease[i]), sdlog = sdlog)
  # internal standards get no biological fold-change AND no group effect (spiked equally)
  mat[i, ] <- c(ctrl_vals, dis_vals)
}

out_df <- data.frame(Molecule = rownames(mat), mat, check.names = FALSE)
write.csv(out_df, "../data/synthetic_lipidomics_intensities.csv", row.names = FALSE)

annot <- data.frame(Sample = samples, group = group, stringsAsFactors = FALSE)
write.csv(annot, "../data/synthetic_sample_annotation.csv", row.names = FALSE)

cat("Wrote", nrow(out_df), "lipid rows x", ncol(mat), "samples\n")
cat("Planted differential (ground truth): PC 34:1 UP 2x, PC 36:2 UP 1.8x, ",
    "PE 36:2 DOWN 0.5x, TG 52:3 UP 1.7x (Disease vs Control)\n")
cat("Planted non-differential: PC 32:0, PC 16:0/18:1, PE 34:1, TG 54:4, ",
    "Cer 18:1;O2/16:0, LPC 16:0\n")
cat("TG class has NO internal standard planted (PC and PE do) -- tests the",
    "no-IS-per-class caveat\n")
