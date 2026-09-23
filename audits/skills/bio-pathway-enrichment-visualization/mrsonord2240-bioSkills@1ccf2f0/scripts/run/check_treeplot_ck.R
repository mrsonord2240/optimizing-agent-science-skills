suppressMessages({
  library(clusterProfiler); library(enrichplot); library(org.Hs.eg.db); library(ggplot2)
})
d <- readRDS("../data/gene_data.rds")
up <- names(d$fc[d$fc > 0]); down <- names(d$fc[d$fc <= 0])
if (length(down) < 4) down <- c(down, d$entrez[!(d$entrez %in% down)][1:(4 - length(down))])
ck <- compareCluster(geneCluster = list(Up = up, Down = down), fun = 'enrichGO',
                      OrgDb = org.Hs.eg.db, ont = 'BP', pvalueCutoff = 0.1)
ck_ts <- pairwise_termsim(ck)
r1 <- tryCatch({ treeplot(ck_ts, showCategory = 20, cluster.params = list(n = 5)); "cluster.params SUCCEEDED" },
               error = function(e) paste("cluster.params ERROR:", conditionMessage(e)))
cat(r1, "\n")
