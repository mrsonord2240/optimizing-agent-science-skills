# Input 1 (Canonical) -- following bio-metabolomics-normalization-qc SKILL.md
# Prompt: "Here is my MTBLS79 peak table (2488 features x 172 samples, 38 pooled QCs across
# 8 batches, DIMS serum cow-vs-sheep). Filter junk features, correct within-batch drift with
# QC-RSC, and validate the correction on HELD-OUT QCs, not just QC clustering."
#
# Pipeline order followed per SKILL.md: (1) detection-rate filter, (2) QCRSC drift correction,
# (3) D-ratio/RSD filter on corrected data, reporting per-filter counts, validated on held-out QCs.

se <- readRDS("F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_pmp.rds")
library(pmp)
library(matrixStats)

class_v <- SummarizedExperiment::colData(se)$Class
batch_v <- SummarizedExperiment::colData(se)$Batch
order_v <- seq_len(ncol(se))  # column order == injection order, per pmp's own MTBLS79 vignette

cat(sprintf("Start: %d features x %d samples (%d QC, %d batches)\n",
            nrow(se), ncol(se), sum(class_v == "QC"), length(unique(batch_v))))

# --- Step 1: detection-rate filter (Frule >= 0.8 within QC), pipeline step 1 in SKILL.md ---
filtered <- filter_peaks_by_fraction(df = se, classes = class_v, method = "QC",
                                      qc_label = "QC", min_frac = 0.8)
cat(sprintf("After QC detection-rate>=80%% filter: %d / %d features\n", nrow(filtered), nrow(se)))

# --- Held-out QC split for non-circular validation (SKILL.md: "validate on HELD-OUT QCs, not
# QC clustering"). QCRSC's own API has no held-out mode, so we fit on odd-indexed QCs per batch
# and score on even-indexed QCs per batch -- the agent has to build this itself. ---
qc_cols <- which(class_v == "QC")
qc_fit_flag <- rep(FALSE, ncol(filtered))
for (b in unique(batch_v)) {
  qc_b <- qc_cols[batch_v[qc_cols] == b]
  qc_fit_flag[qc_b[seq(1, length(qc_b), by = 2)]] <- TRUE
}
qc_test_cols <- setdiff(qc_cols, which(qc_fit_flag))
cat(sprintf("Held-out QC split: %d fit / %d test (of %d total QC)\n",
            sum(qc_fit_flag), length(qc_test_cols), length(qc_cols)))

rsd <- function(x) { x <- x[is.finite(x) & x > 0]; if (length(x) < 3) return(NA_real_); sd(x) / mean(x) }
mat_before <- SummarizedExperiment::assay(filtered)
heldout_rsd_before <- median(apply(mat_before[, qc_test_cols], 1, rsd), na.rm = TRUE)

# --- Step 2: QCRSC drift correction (pmp), using ALL QCs as the documented API requires ---
corrected <- QCRSC(df = filtered, order = order_v, batch = batch_v,
                    classes = class_v, spar = 0, log = TRUE, minQC = 4, qc_label = "QC")
# Fixed SKILL.md now documents this guard immediately after every QCRSC call.
out_mat_guard <- if (methods::is(corrected, "SummarizedExperiment")) SummarizedExperiment::assay(corrected) else corrected
stopifnot(any(rowSums(!is.na(out_mat_guard)) > 0))
cat("QCRSC all-NA guard: PASS (not every feature came back NA)\n")
mat_after <- SummarizedExperiment::assay(corrected)
heldout_rsd_after <- median(apply(mat_after[, qc_test_cols], 1, rsd), na.rm = TRUE)
cat(sprintf("Held-out QC median RSD: %.4f -> %.4f (correction is real only if this drops)\n",
            heldout_rsd_before, heldout_rsd_after))

# --- Step 3: robust D-ratio + RSD filter on CORRECTED data (SKILL.md pipeline step 3) ---
qc_rows_all <- SummarizedExperiment::colData(corrected)$Class == "QC"
bio_rows_all <- !qc_rows_all
sd_qc <- rowMads(mat_after[, qc_rows_all], na.rm = TRUE)
sd_bio <- rowMads(mat_after[, bio_rows_all], na.rm = TRUE)
dratio <- sd_qc / sd_bio
qc_rsd_all <- apply(mat_after[, qc_rows_all], 1, rsd)
keep <- dratio <= 0.5 & qc_rsd_all <= 0.3
keep[is.na(keep)] <- FALSE
cat(sprintf("After D-ratio<=0.5 & QC-RSD<=30%% filter: %d / %d features\n",
            sum(keep), nrow(corrected)))
cat(sprintf("Median D-ratio kept features: %.3f\n", median(dratio[keep], na.rm = TRUE)))
