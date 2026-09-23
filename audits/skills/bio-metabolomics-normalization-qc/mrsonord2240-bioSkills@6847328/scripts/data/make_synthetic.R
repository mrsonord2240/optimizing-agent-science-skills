# Synthetic dataset generator shared across audit inputs 2-7.
# Mirrors the Skill's own examples/normalize_data.R generative model (drift + dilution + MNAR),
# extended with a batch-confound knob (input 5) and a controllable QC density (input 4).
# All data here is SYNTHETIC, generated for this audit only.

make_dataset <- function(n_features = 150, n_bio = 60, n_qc_per_batch = 6, n_batches = 3,
                          confound_group_with_batch = FALSE, seed = 42) {
  set.seed(seed)
  true_abundance <- 2^rnorm(n_features, mean = 10, sd = 2)
  effect <- rep(1, n_features); effect[1:15] <- 1.6  # 10% features truly different

  rows <- list(); row_i <- 1
  batch_v <- integer(0); order_v <- integer(0); class_v <- character(0); group_v <- character(0)
  mat_list <- list()
  bio_per_batch <- ceiling(n_bio / n_batches)
  global_order <- 0

  for (b in seq_len(n_batches)) {
    if (confound_group_with_batch) {
      # Group perfectly determined by batch -- the unwinnable confound the Skill warns about.
      grp_this_batch <- if (b <= ceiling(n_batches / 2)) "control" else "case"
      groups_b <- rep(grp_this_batch, bio_per_batch)
    } else {
      groups_b <- rep(c("control", "case"), length.out = bio_per_batch)
    }
    drift_slope <- rnorm(n_features, mean = 0.01 * b, sd = 0.015)
    dilution_b <- 2^rnorm(bio_per_batch, sd = 0.3)

    # Interleave QCs every ~5 samples, bracketing both ends of the batch.
    qc_positions <- round(seq(1, bio_per_batch + n_qc_per_batch, length.out = n_qc_per_batch))
    total_b <- bio_per_batch + n_qc_per_batch
    is_qc_b <- seq_len(total_b) %in% qc_positions
    bio_idx <- 0
    for (pos in seq_len(total_b)) {
      global_order <- global_order + 1
      noise <- 2^rnorm(n_features, sd = 0.08)
      drift <- 1 + drift_slope * pos
      if (is_qc_b[pos]) {
        vals <- true_abundance * drift * noise
        class_v <- c(class_v, "QC"); group_v <- c(group_v, "QC")
      } else {
        bio_idx <- bio_idx + 1
        fold <- ifelse(groups_b[bio_idx] == "case", effect, 1)
        vals <- true_abundance * fold * drift * noise * dilution_b[bio_idx]
        class_v <- c(class_v, "Sample"); group_v <- c(group_v, groups_b[bio_idx])
      }
      mat_list[[row_i]] <- vals
      batch_v <- c(batch_v, b); order_v <- c(order_v, global_order)
      row_i <- row_i + 1
    }
  }
  mat <- do.call(rbind, mat_list)
  colnames(mat) <- paste0("M", seq_len(n_features))
  rownames(mat) <- paste0("S", seq_len(nrow(mat)))
  list(mat = mat, batch = batch_v, order = order_v, class = class_v, group = group_v,
       true_abundance = true_abundance, effect = effect)
}

inject_missingness <- function(mat, true_abundance, n_mnar = 15, n_mar = 15, seed = 43) {
  set.seed(seed)
  mnar_features <- order(true_abundance)[1:n_mnar]           # low-abundance -> left-censored
  mar_features <- sample(setdiff(seq_len(ncol(mat)), mnar_features), n_mar)  # random -> MAR
  for (f in mnar_features) {
    lod <- quantile(mat[, f], 0.4)
    mat[mat[, f] < lod, f] <- NA
  }
  for (f in mar_features) {
    drop_idx <- sample(nrow(mat), size = round(0.2 * nrow(mat)))
    mat[drop_idx, f] <- NA
  }
  list(mat = mat, mnar_features = mnar_features, mar_features = mar_features)
}
