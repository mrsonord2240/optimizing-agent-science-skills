suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(org.Hs.eg.db)
})

cat("enrichplot=", as.character(packageVersion("enrichplot")), "\n", sep = "")
print(methods("treeplot"))
print(formals(getMethod("treeplot", "enrichResult")))
print(formals(getMethod("treeplot", "compareClusterResult")))

d <- readRDS("../data/gene_data.rds")
up <- names(d$fc[d$fc > 0])
down <- names(d$fc[d$fc <= 0])
ego <- enrichGO(up, OrgDb = org.Hs.eg.db, ont = "BP", pvalueCutoff = 0.1, qvalueCutoff = 0.2)
ego_ts <- pairwise_termsim(ego)
ck <- compareCluster(geneCluster = list(Up = up, Down = down), fun = "enrichGO",
                     OrgDb = org.Hs.eg.db, ont = "BP", pvalueCutoff = 0.1)
ck_ts <- pairwise_termsim(ck)

probe <- function(label, expr) {
  result <- tryCatch({ force(expr); "SUCCEEDED" }, error = function(e) paste("ERROR:", conditionMessage(e)))
  cat(label, result, "\n")
}
probe("enrichResult nCluster", treeplot(ego_ts, showCategory = 20, nCluster = 5))
probe("enrichResult cluster.params", treeplot(ego_ts, showCategory = 20, cluster.params = list(n = 5)))
probe("compareClusterResult nCluster", treeplot(ck_ts, showCategory = 20, nCluster = 5))
probe("compareClusterResult cluster.params", treeplot(ck_ts, showCategory = 20, cluster.params = list(n = 5)))
