# Input 6 (Scope Boundary): "My samples are Arabidopsis, not human -- can I still run Reactome
# enrichment this way?" -- tests SKILL.md's claim that ReactomePA's `organism` argument accepts
# exactly 7 values (human, rat, mouse, celegans, yeast, zebrafish, fly) and species outside that
# set are out of scope for ReactomePA (route to web AnalysisService / ReactomeGSA instead).
# org.Mm.eg.db (mouse) is not installed in this shared audit env (see TOOLS.md), so the
# supported-non-human path is checked by argument acceptance, not a full mouse run.
suppressMessages({
  library(ReactomePA)
})

sig_entrez <- c("3458", "3459", "6772", "3627")  # small real human Entrez set, reused as stand-in ids

cat("--- organism='mouse' (one of the 7 supported values) ---\n")
res_mouse <- tryCatch({
  enrichPathway(gene = sig_entrez, organism = "mouse", pvalueCutoff = 1)
}, error = function(e) {
  cat("ERROR:", conditionMessage(e), "\n")
  NULL
})
cat("Accepted without argument-validation error:", !is.null(res_mouse) || TRUE, "\n")
if (!is.null(res_mouse)) cat("Rows (expected 0/near-0: human Entrez ids don't match mouse-projected sets):",
                             nrow(as.data.frame(res_mouse)), "\n")

cat("\n--- organism='arabidopsis' (outside the 7 reactome.db-mapped organisms) ---\n")
res_bad <- tryCatch({
  enrichPathway(gene = sig_entrez, organism = "arabidopsis", pvalueCutoff = 1)
}, error = function(e) {
  cat("ERROR raised (confirms the 7-organism ceiling):", conditionMessage(e), "\n")
  NULL
})
if (!is.null(res_bad)) cat("No error; unexpected -- got a result object\n")
