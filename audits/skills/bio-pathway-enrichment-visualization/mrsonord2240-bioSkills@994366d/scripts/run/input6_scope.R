# Input 6 (Scope Boundary) -- "I have a flat list of 50 significant GO IDs and p-values that came
# out of a different enrichment tool (not clusterProfiler) -- not an R object, just two columns in a
# CSV. Can you run pairwise_termsim and make me an emapplot showing which of these are really the
# same biological theme?"
#
# This probes the Decision Tree row: "Flat GO-ID + p-value list from a non-clusterProfiler tool ->
# REVIGO (treemap / MDS) -> external semantic collapse". The correct agent behavior per SKILL.md is
# to decline to force this through emapplot/pairwise_termsim (which need a clusterProfiler S4
# enrichResult/gseaResult, not a bare data.frame) and redirect to REVIGO instead. This script checks
# whether that redirect is the ONLY reasonable path, i.e. whether a naive agent could get away with
# just wrapping the flat list in a fake enrichResult and calling pairwise_termsim/emapplot on it.
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(methods)
})

# A flat GO-ID + p-value data.frame, exactly what the prompt describes -- NOT a clusterProfiler object.
flat <- data.frame(
  ID = c('GO:0007049','GO:0000278','GO:0006260','GO:0051301','GO:0007067'),
  Description = c('cell cycle','mitotic cell cycle','DNA replication','cell division','mitosis'),
  pvalue = c(1e-8, 1e-7, 1e-6, 1e-5, 1e-4)
)

cat("Class of the flat input:", class(flat), "\n")
cat("Is it an enrichResult?", is(flat, "enrichResult"), "\n")

# Attempt the naive path: does pairwise_termsim even accept a bare data.frame?
r1 <- tryCatch({ pairwise_termsim(flat); "pairwise_termsim(data.frame) SUCCEEDED (unexpected)" },
                error = function(e) paste("pairwise_termsim(data.frame) ERROR:", conditionMessage(e)))
cat(r1, "\n")

# Does emapplot accept a bare data.frame?
r2 <- tryCatch({ emapplot(flat); "emapplot(data.frame) SUCCEEDED (unexpected)" },
                error = function(e) paste("emapplot(data.frame) ERROR:", conditionMessage(e)))
cat(r2, "\n")

# What would it take to fake an enrichResult? Inspect the S4 class's required slots.
cat("enrichResult slots required:", paste(slotNames("enrichResult"), collapse=", "), "\n")
cat("-> a flat 3-column ID/Description/pvalue table cannot be coerced into this without inventing\n")
cat("   GeneRatio, BgRatio, geneID, Count and the gene universe -- data this prompt does not supply.\n")
cat("CONCLUSION: SKILL.md's Decision Tree redirect to REVIGO for a flat GO-ID+p-value list from a\n")
cat("non-clusterProfiler tool is the only viable path; pairwise_termsim/emapplot genuinely require\n")
cat("a clusterProfiler S4 object and cannot be coerced from a flat data.frame.\n")
