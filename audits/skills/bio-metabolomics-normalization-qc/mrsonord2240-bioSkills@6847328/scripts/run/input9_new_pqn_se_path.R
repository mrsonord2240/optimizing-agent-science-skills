# Input 9 (NEW -- auditor-authored, not in the pre-fix audit) -- Prompt:
# "My peak table is already a SummarizedExperiment (the object xcms-preprocessing hands off).
# PQN-normalize it and pull the per-sample factor the way your Skill documents for that case."
#
# The fix log verified the PLAIN-MATRIX path (attr(normalized,'flags')[,'pqn_coef']) with a
# real run and a 2.8e-14 reconstruction check. The commented-out second line in SKILL.md
# (SummarizedExperiment::colData(normalized)$pqn_coef) is the documented alternative for
# SummarizedExperiment input -- and per the fix log, was NOT independently run. Test it here,
# since this Skill's real upstream handoff (xcms-preprocessing) produces SummarizedExperiment
# objects, not plain matrices, so this is the MORE common real path, not a rare corner case.

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
suppressMessages(library(pmp))
suppressMessages(library(SummarizedExperiment))

d <- make_dataset(n_features = 50, n_bio = 30, n_qc_per_batch = 5, n_batches = 1, seed = 88)
fmat <- t(d$mat)  # features in rows, samples in columns
classes <- d$class
is_qc <- classes == "QC"

set.seed(89)
dil <- 2^rnorm(ncol(fmat), sd = 0.5)
dil[is_qc] <- 1
fmat_dil <- sweep(fmat, 2, dil, "*")

se <- SummarizedExperiment(assays = list(counts = fmat_dil),
                            colData = DataFrame(Class = classes))

norm_se <- tryCatch(
  pqn_normalisation(df = se, classes = SummarizedExperiment::colData(se)$Class, qc_label = "QC"),
  error = function(e) { cat("pqn_normalisation(SummarizedExperiment) errored:", conditionMessage(e), "\n"); NULL }
)

if (!is.null(norm_se)) {
  cat("pqn_normalisation() accepted a SummarizedExperiment input.\n")
  cat("colData(norm_se) columns:", paste(colnames(SummarizedExperiment::colData(norm_se)), collapse = ", "), "\n")
  factor_se <- tryCatch(SummarizedExperiment::colData(norm_se)$pqn_coef,
                          error = function(e) NULL)
  if (is.null(factor_se) || all(is.na(factor_se))) {
    cat("FINDING: SKILL.md's documented SummarizedExperiment path\n")
    cat("  `colData(normalized)$pqn_coef` returned NULL/NA -- the documented alternative for the\n")
    cat("  MORE common real input type (xcms-preprocessing's own output object) does not work as\n")
    cat("  written, even though the plain-matrix 'flags' path was verified.\n")
  } else {
    bio_idx <- which(!is_qc)
    cor_dil <- suppressWarnings(cor(factor_se[bio_idx], dil[bio_idx]))
    cat(sprintf("colData(normalized)$pqn_coef present: length=%d, vs true dilution r=%.3f\n",
                length(factor_se), cor_dil))
    assay_mat <- SummarizedExperiment::assay(norm_se)
    recon_err <- max(abs(sweep(assay_mat, 2, factor_se, "*") - fmat_dil), na.rm = TRUE)
    cat(sprintf("Reconstruction check (normalized * factor == input): max abs error = %.2e\n", recon_err))
  }
} else {
  cat("FINDING: pqn_normalisation() does not accept a SummarizedExperiment `df` argument at all in\n")
  cat("this installed pmp version -- SKILL.md's commented alternative line assumes an API surface\n")
  cat("that doesn't exist here; introspecting is required (per SKILL.md's own Version Compatibility note).\n")
}
