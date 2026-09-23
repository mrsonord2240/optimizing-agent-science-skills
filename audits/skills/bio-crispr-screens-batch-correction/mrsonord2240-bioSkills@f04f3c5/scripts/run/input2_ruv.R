# Input 2 (Variant A) -- POST-FIX regression test, bio-crispr-screens-batch-correction.
# Real request simulated: "I don't know where my technical batch is coming from,
# but my NTCs look shifted across samples. Use RUV with the NTC sgRNAs as
# negative controls to remove it."
#
# Regression target: pre-fix P1 #2 -- SKILL.md's RUV cIdx was built with which()
# (integer positions), which fails S4 dispatch against a SeqExpressionSet. The
# current SKILL.md now uses character rownames. This is a VERBATIM transcription
# of the current "RUV (Remove Unwanted Variation)" code block in run/skill-copy/SKILL.md.

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

# === Current (post-fix) SKILL.md pattern, verbatim ===
ntc_rownames <- rownames(counts_df)[rownames(counts_df) %in% ntc_sgrna_names]
stopifnot(length(ntc_rownames) > 0)
seqset <- newSeqExpressionSet(counts = as.matrix(counts_df))
ruv_corrected <- RUVg(seqset, cIdx = ntc_rownames, k = 2)
W <- pData(ruv_corrected)
corrected_counts <- normCounts(ruv_corrected)
cat("RUVg ran successfully (no dispatch error). k=2 unwanted factors estimated.\n")
cat(sprintf("Corrected counts matrix: %d x %d\n", nrow(corrected_counts), ncol(corrected_counts)))
cat(sprintf("W factors (pData) shape: %d x %d -- columns: %s\n", nrow(W), ncol(W), paste(colnames(W), collapse=", ")))
stopifnot(all(c("W_1", "W_2") %in% colnames(W)))
stopifnot(!any(is.na(corrected_counts)))

# Confirm the OLD (pre-fix) which()-based pattern still fails the same way, so this
# run is a genuine regression test and not just "new code happens to work".
ntc_indices_OLD <- which(rownames(counts_df) %in% ntc_sgrna_names)
old_result <- tryCatch({
  RUVg(seqset, cIdx = ntc_indices_OLD, k = 2)
  "UNEXPECTED: old integer-index pattern now succeeds"
}, error = function(e) paste0("CONFIRMED still fails as pre-fix bug described: ", conditionMessage(e)))
cat(sprintf("\nRegression check (old which()-based cIdx): %s\n", old_result))

# === Verify: did RUV reduce the (analyst-invisible) true batch separation in the NTCs? ===
ntc_raw <- as.matrix(counts_df[ntc_rownames, ])
ntc_corr <- corrected_counts[ntc_rownames, ]

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
