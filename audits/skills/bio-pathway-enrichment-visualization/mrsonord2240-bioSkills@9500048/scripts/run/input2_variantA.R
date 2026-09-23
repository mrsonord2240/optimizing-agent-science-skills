# Input 2 (Variant A) -- "Plot my gseGO GSEA result the way that keeps the direction (activated
# vs suppressed) -- an overview across all significant pathways and a detailed running-score plot
# for the top one."
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(org.Hs.eg.db)
  library(ggplot2)
})

d <- readRDS("../data/gene_data.rds")

set.seed(123)
gse <- gseGO(geneList = d$ranked, OrgDb = org.Hs.eg.db, ont = 'BP',
             minGSSize = 10, maxGSSize = 500, pvalueCutoff = 0.25, verbose = FALSE)
gse <- setReadable(gse, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')

n_sets <- nrow(as.data.frame(gse))
cat("GSEA significant sets:", n_sets, "\n")
if (n_sets > 0) {
  nes <- as.data.frame(gse)$NES
  cat("NES range:", round(min(nes), 2), "to", round(max(nes), 2),
      "| n positive:", sum(nes > 0), "| n negative:", sum(nes < 0), "\n")
}

out <- "input2_output.pdf"
pdf(out, width = 10, height = 8)

# Direction-preserving overview: NES dotplot (works regardless of ggridges).
p_dot <- tryCatch(
  dotplot(gse, x = 'NES', showCategory = 20, color = 'p.adjust') + ggtitle('GSEA: signed NES'),
  error = function(e) { cat("dotplot(NES) ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(p_dot)) print(p_dot)

# Ridgeplot as literally requested in the prompt / Skill's own Quick Start example.
p_ridge <- tryCatch(
  ridgeplot(gse, showCategory = 20),
  error = function(e) { cat("ridgeplot ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(p_ridge)) print(p_ridge)

# Detailed running-score plot for the top pathway.
p_run <- tryCatch(
  gseaplot2(gse, geneSetID = 1, title = as.data.frame(gse)$Description[1]),
  error = function(e) { cat("gseaplot2 ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(p_run)) print(p_run)

# Confirm the Skill's claim: no barplot method exists for gseaResult (would drop the NES sign).
cat("barplot method exists for gseaResult:", existsMethod("barplot", "gseaResult"), "\n")
p_bar <- tryCatch({ barplot(gse); "SUCCEEDED (unexpected)" },
                   error = function(e) paste("ERROR (expected):", conditionMessage(e)))
cat("barplot(gse) attempt:", p_bar, "\n")

dev.off()
cat("Wrote", out, "\n")
