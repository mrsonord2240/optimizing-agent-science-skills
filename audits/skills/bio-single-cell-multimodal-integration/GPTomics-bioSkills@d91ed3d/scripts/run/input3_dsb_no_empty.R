# Input 3 (Edge): "I only have the filtered/cell matrix, no raw/unfiltered droplets --
# denoise my CITE-seq ADT with DSB anyway."
# Tests the Skill's own Common Errors row: "DSB errors / nonsense output <- Passed a filtered
# cell matrix only (no empty droplets) -> Fix: Supply empty_drop_matrix from the raw matrix."
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(dsb))

d <- readRDS("data/synthetic_cite_seq.rds")
adt_cells <- d$adt_cells

result <- tryCatch({
  # Passing the filtered/cell matrix as BOTH arguments -- the only "empty droplet" matrix a
  # user without a raw/unfiltered file would have on hand -- is the realistic failure mode.
  DSBNormalizeProtein(
    cell_protein_matrix = adt_cells,
    empty_drop_matrix = adt_cells,
    denoise.counts = TRUE,
    use.isotype.control = TRUE,
    isotype.control.name.vec = grep('[Ii]sotype|IgG', rownames(adt_cells), value = TRUE)
  )
}, error = function(e) {
  cat("ERROR raised:", conditionMessage(e), "\n")
  NULL
}, warning = function(w) {
  cat("WARNING raised:", conditionMessage(w), "\n")
  NULL
})

if (!is.null(result)) {
  cat("No error/warning raised. Output range:", round(range(result), 2), "\n")
  cat("This is the 'nonsense output' failure mode the SKILL.md Common Errors table warns about:\n")
  cat("DSB ran to completion but the 'ambient' estimate is computed from real cells, not empties,\n")
  cat("so the background correction is not statistically meaningful.\n")
}
cat("Status: COMPLETED\n")
