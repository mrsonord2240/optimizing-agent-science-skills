# Input 2 (Variant A) -- real end-to-end hand-off: workflow's own Stage2 (pmp) code chained
# into Stage4 (ropls) code, on real MTBLS79 biological data (cow vs sheep serum + 38 QCs, 8 batches).
suppressMessages({library(pmp); library(ropls)})

pm <- as.matrix(read.csv("F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_peak_matrix.csv",
                         row.names = 1, check.names = FALSE))
meta <- read.csv("F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_sample_metadata.csv",
                  row.names = 1, check.names = FALSE)
meta <- meta[colnames(pm), ]
cat("Real MTBLS79 peak matrix:", nrow(pm), "features x", ncol(pm), "samples\n")
cat("Classes:", paste(names(table(meta$Class)), table(meta$Class), sep="=", collapse=", "), "\n\n")

sample_class <- meta$Class
batch_id <- meta$Batch
injection_order <- seq_len(ncol(pm))  # real run order not in this flat export; using column order

# === Workflow SKILL.md Stage 2 code, verbatim structure ===
filtered <- filter_peaks_by_fraction(pm, classes = sample_class, min_frac = 0.5, qc_label = "QC")
cat("After filter_peaks_by_fraction:", nrow(filtered), "of", nrow(pm), "features kept\n")

corrected <- tryCatch(
  QCRSC(df = filtered, order = injection_order, batch = batch_id,
        classes = sample_class, spar = 0, minQC = 5, qc_label = "QC"),
  error = function(e) e)
if (inherits(corrected, "error")) { cat("QCRSC ERROR:", conditionMessage(corrected), "\n"); quit(save="no") }
cat("After QCRSC:", nrow(corrected), "x", ncol(corrected), "\n")

rsd_filtered <- filter_peaks_by_rsd(corrected, max_rsd = 30, classes = sample_class, qc_label = "QC")
cat("After filter_peaks_by_rsd:", nrow(rsd_filtered), "of", nrow(corrected), "features kept\n")

normalized <- pqn_normalisation(rsd_filtered, classes = sample_class, qc_label = "QC")
cat("After pqn_normalisation:", nrow(normalized), "x", ncol(normalized), "(features x samples, orientation preserved)\n\n")

# === Workflow SKILL.md Stage 4 code, verbatim: t(normalized)[study_samples, ] into opls() ===
study_samples <- sample_class != "QC"
study_group <- factor(sample_class[study_samples])
cat("Study design for OPLS-DA: n =", sum(study_samples), "| groups:", paste(levels(study_group), collapse=" vs "), "\n")

x <- t(normalized)[study_samples, ]
cat("Hand-off shape check: t(normalized)[study_samples,] =", nrow(x), "x", ncol(x),
    "(expect samples-in-rows for ropls -- ", nrow(x), "should equal", sum(study_samples), ")\n\n")

cat("=== Running the workflow's own documented opls() call on REAL biological data ===\n")
res <- tryCatch({
  capture.output(
    m <- opls(x, study_group, predI = 1, orthoI = NA, scaleC = "pareto",
              permI = 1000, crossvalI = 7, fig.pdfC = "none", info.txtC = "none")
  )
  m
}, error = function(e) e, warning = function(w) w)

if (inherits(res, "error")) {
  cat("opls() ERROR:", conditionMessage(res), "\n")
} else {
  m <- res
  cat("class(m):", class(m), "| typeC:", m@typeC, "\n")
  sdf <- tryCatch(getSummaryDF(m), error = function(e) e)
  if (inherits(sdf, "error")) {
    cat("getSummaryDF ERROR:", conditionMessage(sdf), "\n")
  } else {
    cat("getSummaryDF rows:", nrow(sdf), "\n")
    print(sdf)
  }
  vip <- tryCatch(getVipVn(m), error = function(e) e)
  cat("getVipVn length:", if(inherits(vip,"error")) paste("ERROR:", conditionMessage(vip)) else length(vip), "\n")
}
