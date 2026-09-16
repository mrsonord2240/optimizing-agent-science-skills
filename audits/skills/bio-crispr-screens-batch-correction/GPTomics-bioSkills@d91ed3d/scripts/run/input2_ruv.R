# Input 2 (Variant A) -- bio-crispr-screens-batch-correction audit.
# Real request simulated: "I don't know where my technical batch is coming from,
# but my NTCs look shifted across samples. Use RUV with the NTC sgRNAs as
# negative controls to remove it."
#
# Runs the Skill's own documented RUVSeq code (SKILL.md "RUV (Remove Unwanted
# Variation)" section) verbatim against a synthetic dataset with a HIDDEN batch
# (the true batch labels are saved separately and NOT passed to RUVg -- only
# the NTC identity is, matching the real-world use case for RUV over ComBat).

suppressMessages(library(RUVSeq))

counts_raw <- read.csv(r"(F:\OpenScience\audits\bio-crispr-screens-batch-correction\data\input2_ruv_counts.csv)",
                        stringsAsFactors = FALSE)
truth <- read.csv(r"(F:\OpenScience\audits\bio-crispr-screens-batch-correction\data\input2_ruv_TRUE_batch_ground_truth.csv)",
                   stringsAsFactors = FALSE)

sample_cols <- truth$sample
rownames(counts_raw) <- counts_raw$guide
counts_df <- counts_raw[, sample_cols]
cat(sprintf("Loaded %d guides x %d samples (synthetic, hidden 2-batch design)\n",
            nrow(counts_df), ncol(counts_df)))

ntc_sgrna_names <- counts_raw$guide[grepl("^NT_", counts_raw$guide)]
cat(sprintf("Identified %d NTC sgRNAs as negative controls\n", length(ntc_sgrna_names)))

# === Skill's own documented pattern, verbatim (see BUG note) ===
ntc_indices <- which(rownames(counts_df) %in% ntc_sgrna_names)
seqset <- newSeqExpressionSet(counts = as.matrix(counts_df))
ruv_result <- tryCatch({
  RUVg(seqset, cIdx = ntc_indices, k = 2)
}, error = function(e) e)
if (inherits(ruv_result, "error")) {
  cat(sprintf("CONFIRMED BUG (SKILL.md code as written): %s\n", conditionMessage(ruv_result)))
  cat("Cause: RUVg's S4 method for x='SeqExpressionSet' requires cIdx='character'\n")
  cat("(control-feature ROWNAMES), but SKILL.md builds cIdx via which(...), which\n")
  cat("returns integer POSITIONS -- there is no registered method for\n")
  cat("x='SeqExpressionSet', cIdx='integer', so dispatch fails outright.\n")
  cat("Fix: use character rownames instead of which() positions:\n")
  cat("  ntc_indices <- rownames(counts_df)[rownames(counts_df) %in% ntc_sgrna_names]\n\n")
}

# Fixed version, used for the rest of this run:
ntc_indices <- rownames(counts_df)[rownames(counts_df) %in% ntc_sgrna_names]
ruv_corrected <- RUVg(seqset, cIdx = ntc_indices, k = 2)
corrected_counts <- normCounts(ruv_corrected)
cat("RUVg ran successfully. k=2 unwanted factors estimated.\n")
cat(sprintf("Corrected counts matrix: %d x %d\n", nrow(corrected_counts), ncol(corrected_counts)))

# === Verify: did RUV reduce the (analyst-invisible) true batch separation in the NTCs? ===
ntc_raw <- as.matrix(counts_df[ntc_indices, ])
ntc_corr <- corrected_counts[ntc_indices, ]

deep_samples <- truth$sample[truth$true_batch_HIDDEN == "deep"]
shallow_samples <- truth$sample[truth$true_batch_HIDDEN == "shallow"]

raw_deep_med <- median(as.matrix(ntc_raw[, deep_samples]))
raw_shallow_med <- median(as.matrix(ntc_raw[, shallow_samples]))
corr_deep_med <- median(ntc_corr[, deep_samples])
corr_shallow_med <- median(ntc_corr[, shallow_samples])

cat(sprintf("\nNTC median counts (raw):       deep=%.1f  shallow=%.1f  ratio=%.3f\n",
            raw_deep_med, raw_shallow_med, raw_shallow_med / raw_deep_med))
cat(sprintf("NTC median counts (corrected):  deep=%.1f  shallow=%.1f  ratio=%.3f\n",
            corr_deep_med, corr_shallow_med, corr_shallow_med / corr_deep_med))
cat(sprintf("Ratio moved toward 1.0 (batch-neutral): %s\n",
            ifelse(abs(1 - corr_shallow_med/corr_deep_med) < abs(1 - raw_shallow_med/raw_deep_med),
                   "YES", "NO")))

# === Check essential-gene condition signal survived (treat vs ctrl on essential genes) ===
essential_guides <- counts_raw$guide[grepl("^Gene_00[0-2][0-9]_", counts_raw$guide)]
ess_idx <- which(rownames(counts_df) %in% essential_guides)
treat_samples <- truth$sample[truth$condition == "treat"]
ctrl_samples <- truth$sample[truth$condition == "ctrl"]

raw_lfc <- log2((rowMeans(as.matrix(counts_df[ess_idx, treat_samples])) + 1) /
                 (rowMeans(as.matrix(counts_df[ess_idx, ctrl_samples])) + 1))
corr_lfc <- log2((rowMeans(corrected_counts[ess_idx, treat_samples]) + 1) /
                  (rowMeans(corrected_counts[ess_idx, ctrl_samples]) + 1))

cat(sprintf("\nEssential-gene guides: mean raw LFC=%.3f, mean RUV-corrected LFC=%.3f (both should be strongly negative -- dropout)\n",
            mean(raw_lfc), mean(corr_lfc)))

write.csv(as.data.frame(corrected_counts),
          r"(F:\OpenScience\audits\bio-crispr-screens-batch-correction\run\out_input2_ruv_corrected_counts.csv)")
cat("\nDone.\n")
