# Input 5 (Stress/multi-part, REGRESSION) -- "Canonicalize my lipid names,
# normalize by class-based internal standard, run differential analysis AND
# lipid set enrichment (class/chain/unsaturation), and give me an honest
# resolution-level report before I write this up."
# Updated post-fix to include the istd-coverage guard (same pattern as
# input1_canonical.R) before normalize_istd(), then continues into
# de_analysis + lsea on the properly-scoped (TG-excluded) data.
suppressMessages(library(lipidr))

raw <- read.csv("../data/synthetic_lipidomics_intensities.csv", check.names = FALSE)
d <- as_lipidomics_experiment(raw)
d <- suppressWarnings(add_sample_annotation(d, "../data/synthetic_sample_annotation.csv"))

istd_coverage <- table(rowData(d)$Class, rowData(d)$istd)
uncovered <- rownames(istd_coverage)[
  !("TRUE" %in% colnames(istd_coverage)) | istd_coverage[, "TRUE"] == 0
]
cat("Uncovered classes:", paste(uncovered, collapse = ", "), "-- excluding from ISTD-normalized reporting\n")
keep <- !is.na(rowData(d)$Class) & !(rowData(d)$Class %in% uncovered)
d <- d[keep, ]

d_istd <- normalize_istd(d, measure = "Area", exclude = "blank", log = TRUE)
de_results <- suppressWarnings(de_analysis(d_istd, Disease - Control, measure = "Area"))

cat("=== lsea() lipid set enrichment (class / chain length / unsaturation) ===\n")
enrich <- tryCatch(
  lsea(de_results, rank.by = "logFC"),
  error = function(e) { cat("lsea() ERROR:", conditionMessage(e), "\n"); NULL }
)

if (!is.null(enrich)) {
  print(class(enrich))
  sig_sets <- tryCatch(
    significant_lipidsets(enrich, p.cutoff = 0.05, size.cutoff = 2),
    error = function(e) { cat("significant_lipidsets() ERROR:", conditionMessage(e), "\n"); NULL }
  )
  print(sig_sets)
  if (!is.null(sig_sets) && length(sig_sets) > 0) {
    plt <- tryCatch(
      plot_enrichment(de_results, sig_sets, annotation = "class", measure = "logFC"),
      error = function(e) { cat("plot_enrichment() ERROR:", conditionMessage(e), "\n"); NULL }
    )
    if (!is.null(plt)) {
      ggplot2::ggsave("../data/input5_enrichment.png", plt, width = 7, height = 5)
      cat("Saved input5_enrichment.png\n")
    }
  } else {
    cat("No significant lipid sets at p<0.05 (expected: small synthetic set is",
        "underpowered for enrichment -- this is a real result, not a bug)\n")
  }
}
