# Input 1 (Canonical, REGRESSION) -- "Load my lipidomics table, normalize
# within class, and find lipids changing between groups (Control vs Disease)."
# Same synthetic dataset as the pre-fix audit (TG has NO internal standard;
# PC and PE do -- i.e. genuinely PARTIAL coverage, not all-or-nothing).
#
# Pre-fix: normalize_istd() silently divided TG by factor=1 (uncorrected) and
# reported it as normalized. Post-fix: SKILL.md's "Class-Based Internal-
# Standard Quantification" section now runs an istd-coverage guard BEFORE
# normalize_istd() and stop()s naming any uncovered class.
#
# This script follows the new SKILL.md pattern verbatim and checks BOTH
# directions: (1) the guard actually stops loud for TG (the dangerous silent
# no-op must now be loud), and (2) after handling the uncovered class the
# guard does NOT refuse the classes that ARE covered (PC, PE) -- partial
# coverage must not become a blanket refusal.
suppressMessages(library(lipidr))

raw <- read.csv("../data/synthetic_lipidomics_intensities.csv", check.names = FALSE)
d <- as_lipidomics_experiment(raw)
cat("Loaded LipidomicsExperiment:", nrow(d), "lipids x", ncol(d), "samples\n")
cat("Classes detected:", paste(unique(rowData(d)$Class), collapse = ", "), "\n")
cat("Flagged as internal standards by lipidr:",
    paste(rownames(d)[rowData(d)$istd], collapse = ", "), "\n\n")

d <- add_sample_annotation(d, "../data/synthetic_sample_annotation.csv")

# --- SKILL.md guard, verbatim pattern ---
istd_coverage_check <- function(dd) {
  istd_coverage <- table(rowData(dd)$Class, rowData(dd)$istd)
  uncovered <- rownames(istd_coverage)[
    !("TRUE" %in% colnames(istd_coverage)) | istd_coverage[, "TRUE"] == 0
  ]
  uncovered
}

uncovered <- istd_coverage_check(d)
cat("=== Step 1: guard on FULL (partial-coverage) dataset ===\n")
cat("Uncovered classes found:", paste(uncovered, collapse = ", "), "\n")

guard_result <- tryCatch({
  if (length(uncovered) > 0) {
    stop(sprintf(
      "No recognized internal standard for class(es): %s -- normalize_istd() would pass these through uncorrected (factor=1), not normalized. Add a labeled standard for this class or exclude it from ISTD-normalized reporting.",
      paste(uncovered, collapse = ", ")
    ))
  }
  "NO_STOP"
}, error = function(e) conditionMessage(e))

cat("Guard fired:", !identical(guard_result, "NO_STOP"), "\n")
cat("Guard message:", guard_result, "\n\n")

stopifnot(!identical(guard_result, "NO_STOP"))   # must have fired
stopifnot(grepl("TG", guard_result))             # must name TG specifically
stopifnot(!grepl("PC[^R]|PE", guard_result) || grepl("TG", guard_result)) # sanity: TG named

# --- Step 2: handle it the way SKILL.md's fix text instructs -- "exclude it
# from ISTD-normalized reporting" -- then confirm PC/PE (the covered classes)
# are NOT refused and still process correctly. ---
cat("=== Step 2: exclude uncovered classes (", paste(uncovered, collapse = ", "),
    ") and unparsed (NA-class) rows, re-check guard, then normalize ===\n", sep = "")
keep <- !is.na(rowData(d)$Class) & !(rowData(d)$Class %in% uncovered)
d_covered <- d[keep, ]
uncovered2 <- istd_coverage_check(d_covered)
cat("Uncovered classes after exclusion:",
    if (length(uncovered2) == 0) "(none)" else paste(uncovered2, collapse = ", "), "\n")
stopifnot(length(uncovered2) == 0)   # guard must NOT false-positive on the covered remainder

d_istd <- normalize_istd(d_covered, measure = "Area", exclude = "blank", log = TRUE)
cat("normalize_istd() completed on covered classes:", nrow(d_istd), "lipids x", ncol(d_istd), "samples\n\n")

de_results <- de_analysis(d_istd, Disease - Control, measure = "Area")
sig_raw <- significant_molecules(de_results, p.cutoff = 0.05, logFC.cutoff = 1)
sig <- unlist(sig_raw, use.names = FALSE)  # significant_molecules() returns a named list keyed by contrast

cat("=== de_analysis results (PC/PE only, TG properly excluded from ISTD reporting) ===\n")
print(de_results[order(de_results$adj.P.Val),
                  c("Molecule", "Class", "logFC", "P.Value", "adj.P.Val")])

cat("\n=== Significant molecules (|log2FC|>1, adj.P<0.05) ===\n")
print(sig)

cat("\n=== Ground-truth check (TG deliberately excluded -- it has no valid IS) ===\n")
planted_up   <- c("PC 34:1", "PC 36:2")
planted_down <- c("PE 36:2")
planted_flat <- c("PC 32:0", "PC 16:0/18:1", "PE 34:1")
cat("Planted UP recovered as significant:",
    paste(planted_up[planted_up %in% sig], collapse = ", "), "\n")
cat("Planted DOWN recovered as significant:",
    paste(planted_down[planted_down %in% sig], collapse = ", "), "\n")
cat("Planted FLAT falsely flagged significant (should be none):",
    paste(planted_flat[planted_flat %in% sig], collapse = "(none)"), "\n")
cat("TG present in ISTD-normalized output (should be FALSE -- excluded, not silently miscorrected):",
    "TG 52:3" %in% de_results$Molecule, "\n")

out_dir <- "../data"
volcano <- plot_results_volcano(de_results, show.labels = FALSE)
ggplot2::ggsave(file.path(out_dir, "input1_volcano.png"), volcano, width = 7, height = 5)
write.csv(de_results, file.path(out_dir, "input1_de_results.csv"), row.names = FALSE)
cat("\nSaved input1_de_results.csv and input1_volcano.png\n")
