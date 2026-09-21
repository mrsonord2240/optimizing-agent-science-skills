# SKILL.md OLO block verbatim + pheatmap/ComplexHeatmap default-equivalence claim ("Reconciliation" row 1), real ALL data
suppressPackageStartupMessages({library(ComplexHeatmap);library(seriation);library(pheatmap);library(ALL);library(Biobase)})
data(ALL); X <- exprs(ALL); mat <- t(scale(t(X[order(apply(X,1,var), decreasing=TRUE)[1:150], 1:40])))
# ---- verbatim ----
dist_rows <- dist(mat)
hc_rows <- hclust(dist_rows, method = 'ward.D2')
olo_rows <- seriate(dist_rows, method = 'OLO', control = list(hclust = hc_rows))

ht <- Heatmap(mat,
        cluster_rows = as.dendrogram(olo_rows[[1]]),
        cluster_columns = TRUE,
        clustering_method_columns = 'ward.D2')
# ---- end ----
pdf(NULL); d <- draw(ht); dev.off()
cat("class(olo_rows[[1]]):", class(olo_rows[[1]])[1], "; row_order == OLO order:", identical(as.integer(row_order(d)), as.integer(get_order(olo_rows[[1]]))), "\n")
# claim: pheatmap and ComplexHeatmap differ by default?
p <- pheatmap(mat, silent = TRUE)
h <- Heatmap(mat); pdf(NULL); dh <- draw(h); dev.off()
cat("pheatmap default rows tree == ComplexHeatmap default rows tree (cophenetic identical):",
    isTRUE(all.equal(as.matrix(cophenetic(p$tree_row)), as.matrix(cophenetic(as.hclust(row_dend(dh))))[p$tree_row$labels, p$tree_row$labels] )), "\n")
p2 <- pheatmap(mat, clustering_method = "ward.D2", silent = TRUE)
cat("pheatmap ward.D2 passes through to hclust: tree method =", p2$tree_row$method, "; heights identical to hclust(dist, ward.D2):",
    isTRUE(all.equal(sort(p2$tree_row$height), sort(hclust(dist(mat), "ward.D2")$height))), "\n")
h2 <- Heatmap(mat, clustering_method_rows = "ward.D2"); pdf(NULL); dh2 <- draw(h2); dev.off()
cat("ComplexHeatmap ward.D2 heights identical:", isTRUE(all.equal(sort(as.hclust(row_dend(dh2))$height), sort(hclust(dist(mat), "ward.D2")$height))), "\n")
