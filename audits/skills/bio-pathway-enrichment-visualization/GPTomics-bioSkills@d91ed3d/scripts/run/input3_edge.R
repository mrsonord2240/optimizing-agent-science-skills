# Input 3 (Edge) -- "My enrichResult only has a couple of significant GO terms after FDR
# correction. Build a gene-concept network for my top terms, colored by log2 fold change, and
# tell me if a term-similarity map even makes sense at this scale."
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(org.Hs.eg.db)
  library(ggplot2)
})

d <- readRDS("../data/gene_data.rds")

# Force a near-empty result: a strict pvalueCutoff on a small, weakly-enriched gene subset.
small_set <- d$entrez[1:6]
ego_small <- enrichGO(gene = small_set, OrgDb = org.Hs.eg.db, ont = 'BP',
                       pvalueCutoff = 0.01, qvalueCutoff = 0.05, readable = TRUE)
n <- nrow(as.data.frame(ego_small))
cat("Significant terms at strict cutoff:", n, "\n")

out <- "input3_output.pdf"
pdf(out, width = 9, height = 7)

if (n == 0) {
  cat("No significant terms survive this cutoff -- nothing to plot. ",
      "Relaxing pvalueCutoff for a usable demonstration.\n")
  ego_small <- enrichGO(gene = small_set, OrgDb = org.Hs.eg.db, ont = 'BP',
                         pvalueCutoff = 0.2, qvalueCutoff = 0.2, readable = TRUE)
  n <- nrow(as.data.frame(ego_small))
  cat("Terms at relaxed cutoff:", n, "\n")
}

if (n >= 1) {
  fc_sub <- d$fc[small_set]
  p_cnet <- tryCatch(
    cnetplot(ego_small, showCategory = min(5, n), foldChange = fc_sub),
    error = function(e) { cat("cnetplot ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(p_cnet)) print(p_cnet)
}

# The actual edge-case question: does pairwise_termsim/emapplot make sense with this few terms?
p_ts <- tryCatch({ pairwise_termsim(ego_small) }, error = function(e) {
  cat("pairwise_termsim ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(p_ts)) {
  p_emap <- tryCatch(emapplot(p_ts), error = function(e) {
    cat("emapplot ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(p_emap)) print(p_emap)
}
cat("n terms available for similarity map:", n, "-- a map is only informative with several terms;",
    "at n<=2 there is nothing for redundancy structure to show.\n")

dev.off()
cat("Wrote", out, "\n")
