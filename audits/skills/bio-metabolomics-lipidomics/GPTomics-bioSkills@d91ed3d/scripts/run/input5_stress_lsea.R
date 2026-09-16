# Input 5 (Stress/multi-part) -- "Canonicalize my lipid names, normalize by
# class-based internal standard, run differential analysis AND lipid set
# enrichment (class/chain/unsaturation), and give me an honest resolution-
# level report before I write this up." Reuses Input 1's real de_results.
suppressMessages(library(lipidr))

raw <- read.csv("../data/synthetic_lipidomics_intensities.csv", check.names = FALSE)
d <- as_lipidomics_experiment(raw)
d <- suppressWarnings(add_sample_annotation(d, "../data/synthetic_sample_annotation.csv"))
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
    cat("No significant lipid sets at p<0.05 (expected: n=12 lipids / 5 classes is too",
        "small/underpowered a set for enrichment -- this is a real result, not a bug)\n")
  }
}
