# Input 5 (Stress) -- "Give me the full modeling-choice figure set from my enrichGO BP result:
# raw top-20 dotplot AND simplify()+dotplot; pairwise_termsim -> emapplot and treeplot; a
# gene-concept network for the top 6 terms colored by fold change; a heatplot; and an upsetplot of
# gene overlaps. Order the dotplot by fold enrichment instead of GeneRatio and explain why that
# differs from the default in the caption."
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(org.Hs.eg.db)
  library(ggplot2)
})

d <- readRDS("../data/gene_data.rds")

ego <- enrichGO(gene = d$entrez, OrgDb = org.Hs.eg.db, ont = 'BP',
                 pvalueCutoff = 0.05, qvalueCutoff = 0.2, readable = TRUE)
n_raw <- nrow(as.data.frame(ego))
cat("Raw significant terms:", n_raw, "\n")

out <- "input5_output.pdf"
pdf(out, width = 11, height = 9)
plots_made <- c()

try_plot <- function(name, expr) {
  p <- tryCatch(expr, error = function(e) { cat(name, "ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(p)) { print(p); plots_made <<- c(plots_made, name) }
}

try_plot("raw_dotplot", dotplot(ego, showCategory = 20) + ggtitle('Raw top-20'))

ego_simple <- simplify(ego, cutoff = 0.7, by = 'p.adjust', select_fun = min)
try_plot("simplified_dotplot", dotplot(ego_simple, showCategory = 20) + ggtitle('Simplified'))

# GeneRatio vs FoldEnrichment: compute FoldEnrichment manually to verify dotplot's x='FoldEnrichment'
# actually reorders (this is the caption claim the prompt asks the agent to explain).
df <- as.data.frame(ego)
gr <- sapply(strsplit(df$GeneRatio, '/'), function(x) as.numeric(x[1]) / as.numeric(x[2]))
bgr <- sapply(strsplit(df$BgRatio, '/'), function(x) as.numeric(x[1]) / as.numeric(x[2]))
fold <- gr / bgr
cat("GeneRatio vs computed FoldEnrichment -- Spearman rho:",
    round(cor(gr, fold, method = 'spearman'), 3),
    "(1.0 would mean the two orderings never differ)\n")

try_plot("foldenrichment_dotplot",
         dotplot(ego, x = 'FoldEnrichment', showCategory = 20) + ggtitle('Ordered by fold enrichment'))

ego_ts <- pairwise_termsim(ego)
try_plot("emapplot", emapplot(ego_ts, showCategory = 30))
try_plot("treeplot", treeplot(ego_ts, showCategory = 20, nCluster = 5))
try_plot("cnetplot", cnetplot(ego, showCategory = 6, foldChange = d$fc))
try_plot("heatplot", heatplot(ego, foldChange = d$fc, showCategory = 15))
try_plot("upsetplot", upsetplot(ego, n = 10))

dev.off()
cat("Plots produced:", paste(plots_made, collapse = ', '), "\n")
cat("Wrote", out, "\n")
