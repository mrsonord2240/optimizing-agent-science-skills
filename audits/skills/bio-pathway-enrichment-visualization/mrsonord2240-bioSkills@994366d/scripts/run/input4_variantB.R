# Input 4 (Variant B) -- "I ran compareCluster across my up- and down-regulated gene sets and want
# a faceted dotplot comparing them. Also show the redundancy structure with an enrichment map and
# a treeplot with 5 named clusters."
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(org.Hs.eg.db)
  library(ggplot2)
})

d <- readRDS("../data/gene_data.rds")

# Synthetic up/down gene lists from the same cell-cycle-biased pool (split by fabricated FC sign).
up <- names(d$fc[d$fc > 0])
down <- names(d$fc[d$fc <= 0])
# Guarantee both non-trivial for compareCluster to have something to facet.
if (length(down) < 4) down <- c(down, d$entrez[!(d$entrez %in% down)][1:(4 - length(down))])
gene_clusters <- list(Up = up, Down = down)
cat("Up:", length(up), "genes | Down:", length(down), "genes\n")

ck <- compareCluster(geneCluster = gene_clusters, fun = 'enrichGO',
                      OrgDb = org.Hs.eg.db, ont = 'BP', pvalueCutoff = 0.1)
n <- nrow(as.data.frame(ck))
cat("compareCluster rows:", n, "\n")

out <- "input4_output.pdf"
pdf(out, width = 11, height = 9)

if (n > 0) {
  p_facet <- dotplot(ck) + ggtitle('Up vs Down -- faceted dotplot')
  print(p_facet)

  ck_ts <- tryCatch(pairwise_termsim(ck), error = function(e) {
    cat("pairwise_termsim(compareClusterResult) ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(ck_ts)) {
    p_emap <- tryCatch(emapplot(ck_ts, showCategory = 30), error = function(e) {
      cat("emapplot ERROR:", conditionMessage(e), "\n"); NULL })
    if (!is.null(p_emap)) print(p_emap)

    p_tree <- tryCatch(treeplot(ck_ts, showCategory = 20, nCluster = 5), error = function(e) {
      cat("treeplot ERROR:", conditionMessage(e), "\n"); NULL })
    if (!is.null(p_tree)) print(p_tree)
  }
} else {
  cat("No significant terms in either cluster at this cutoff -- nothing to facet.\n")
}

dev.off()
cat("Wrote", out, "\n")
