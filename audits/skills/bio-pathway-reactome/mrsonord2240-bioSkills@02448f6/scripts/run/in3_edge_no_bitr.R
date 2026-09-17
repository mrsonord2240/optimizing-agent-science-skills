# Input 3 (Edge): "Run Reactome enrichment directly on my significant gene symbols, don't
# bother converting them" -- an off-spec request that skips the mandatory bitr step. Verifies
# SKILL.md's documented failure mode: "enrichPathway has NO keyType argument ... non-ENTREZ ids
# match nothing ... zero rows, no error" (Per-Method Failure Modes section).
suppressMessages({
  library(ReactomePA)
})

sig_symbols <- read.csv("../data/significant_genes.csv", stringsAsFactors = FALSE)$SYMBOL
bg_symbols  <- read.csv("../data/background_genes.csv", stringsAsFactors = FALSE)$SYMBOL

result <- tryCatch({
  enrichPathway(gene = sig_symbols, organism = "human", universe = bg_symbols,
               pvalueCutoff = 0.05, readable = FALSE)
}, error = function(e) {
  cat("ERROR raised:", conditionMessage(e), "\n")
  NULL
})

if (!is.null(result)) {
  df <- as.data.frame(result)
  cat("No error raised. Rows returned:", nrow(df), "\n")
  cat("Claim in SKILL.md ('zero rows, no error') confirmed:", nrow(df) == 0, "\n")
}
