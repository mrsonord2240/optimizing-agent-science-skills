.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(dsb)

# Independent synthetic data (different seed/shape from the audit's own
# make_synthetic_cite_seq.R) for a fresh regression check of the median-ADT-count
# guard the fixer added to SKILL.md's CITE-seq DSB block.
set.seed(2026)
n_adt <- 10
n_cells <- 200
n_empty <- 1500
adt_names <- paste0("ADT", 1:n_adt)

# real cells: high ADT signal
adt_cells <- matrix(rpois(n_adt * n_cells, lambda = 60), nrow = n_adt, ncol = n_cells)
rownames(adt_cells) <- adt_names
colnames(adt_cells) <- paste0("CELL-", 1:n_cells)

# true empty droplets: low ambient-only signal
adt_empty_real <- matrix(rpois(n_adt * n_empty, lambda = 4), nrow = n_adt, ncol = n_empty)
rownames(adt_empty_real) <- adt_names
colnames(adt_empty_real) <- paste0("EMPTY-", 1:n_empty)

# misuse case: pass a second slice of the CELL matrix as "empty_drop_matrix"
adt_misuse <- adt_cells[, 101:200]
adt_cells_sub <- adt_cells[, 1:100]

# borderline case: empty droplets with count level right at ~50% of cell median
# (a case the fixer did not report testing) to see whether the guard's 0.5x cutoff
# is reasonable or trivially gamed
med_target <- median(colSums(adt_cells)) * 0.5
lambda_borderline <- med_target / n_adt
adt_borderline <- matrix(rpois(n_adt * n_empty, lambda = lambda_borderline), nrow = n_adt, ncol = n_empty)
rownames(adt_borderline) <- adt_names
colnames(adt_borderline) <- paste0("BORD-", 1:n_empty)

guard <- function(cells, empty, label) {
  med_cells <- median(colSums(cells))
  med_empty <- median(colSums(empty))
  ratio <- med_empty / med_cells
  cat(sprintf("[%s] median cells=%.1f median empty=%.1f ratio=%.3f -> ", label, med_cells, med_empty, ratio))
  ok <- tryCatch({
    if (med_empty >= med_cells * 0.5) {
      stop(sprintf(
        "empty_drop_matrix does not look like empty droplets (median total ADT %.1f vs cells %.1f) -- DSB needs the raw/unfiltered matrix's non-cell barcodes, not a second cell matrix.",
        med_empty, med_cells))
    }
    TRUE
  }, error = function(e) {
    cat("GUARD STOPPED: ", conditionMessage(e), "\n")
    FALSE
  })
  if (ok) cat("GUARD PASSED (would proceed to DSBNormalizeProtein)\n")
  ok
}

cat("=== Case 1: real empty droplets (should PASS guard, then DSB should run and denoise) ===\n")
pass1 <- guard(adt_cells, adt_empty_real, "real-empty")
if (pass1) {
  out <- DSBNormalizeProtein(cell_protein_matrix = adt_cells, empty_drop_matrix = adt_empty_real,
                              denoise.counts = FALSE)
  cat(sprintf("DSB output range: %.2f .. %.2f\n", min(out), max(out)))
}

cat("\n=== Case 2: misuse -- second cell slice passed as empty_drop_matrix (should STOP guard) ===\n")
pass2 <- guard(adt_cells_sub, adt_misuse, "misuse-cell-as-empty")

cat("\n=== Case 3: borderline -- empty droplets at exactly the 0.5x cutoff (documents guard's edge behavior) ===\n")
pass3 <- guard(adt_cells, adt_borderline, "borderline-0.5x")

cat("\nSummary: real-empty PASS=", pass1, " misuse STOP=", !pass2, " borderline PASS=", pass3, "\n")
