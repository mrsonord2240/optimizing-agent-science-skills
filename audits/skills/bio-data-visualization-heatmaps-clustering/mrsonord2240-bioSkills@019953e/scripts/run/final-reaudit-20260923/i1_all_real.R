# INPUT 1 (canonical): real ALL leukemia microarray (Bioconductor 'ALL', 12625 x 128), top-variable genes,
# row z-score, ward.D2 + OLO, BT (B/T lineage) + mol.biol annotation. Code follows SKILL.md blocks (OLO block, annotation block, color-bounds).
suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize);library(seriation);library(ALL);library(Biobase);library(scico)})
data(ALL)
pd <- pData(ALL)
keep <- !is.na(pd$mol.biol) & pd$mol.biol %in% c("BCR/ABL","NEG","ALL1/AF4","E2A/PBX1")
X <- exprs(ALL)[, keep]; md <- pd[keep, ]
md$lineage <- ifelse(substr(as.character(md$BT),1,1)=="B", "B-cell", "T-cell")
vars <- apply(X, 1, var); top <- order(vars, decreasing = TRUE)[1:200]
mat <- t(scale(t(X[top, ])))                       # row z-score
cat("matrix:", dim(mat), " row mean max abs:", signif(max(abs(rowMeans(mat))),2), " row sd range:", range(round(apply(mat,1,sd),3)), "\n")
bounds <- quantile(abs(mat), 0.99)
vik <- scico(3, palette = "vik")                   # Crameri vik (diverging), ends + centre
col_fun <- colorRamp2(c(-bounds, 0, bounds), c(vik[1], vik[2], vik[3]))
cat("bounds:", round(bounds,3), " frac |z|>bounds:", round(mean(abs(mat)>bounds),4), "\n")
# OLO block from SKILL.md
dist_rows <- dist(mat)
hc_rows <- hclust(dist_rows, method = 'ward.D2')
olo_rows <- seriate(dist_rows, method = 'OLO', control = list(hclust = hc_rows))
dend_rows <- as.dendrogram(olo_rows[[1]])
ha_col <- HeatmapAnnotation(Lineage = md$lineage, Fusion = as.character(md$mol.biol),
   col = list(Lineage = c(`B-cell`='#56B4E9', `T-cell`='#D55E00'),
              Fusion  = c(`BCR/ABL`='#009E73', NEG='#999999', `ALL1/AF4`='#CC79A7', `E2A/PBX1`='#F0E442')),
   annotation_name_gp = gpar(fontsize = 8))
ht <- Heatmap(mat, name = "Z-score", col = col_fun, cluster_rows = dend_rows,
   cluster_columns = TRUE, clustering_method_columns = 'ward.D2', clustering_distance_columns = 'euclidean',
   top_annotation = ha_col, show_row_names = FALSE, show_column_names = FALSE, column_split = 2, use_raster = TRUE, raster_quality = 5)
png("i1_all_heatmap.png", 1000, 800, res = 110); ht_d <- draw(ht, merge_legends = TRUE); dev.off()
# ---------------- assertions against the numbers ----------------
ro <- row_order(ht_d); co <- column_order(ht_d)
cat("row_order is a full permutation:", identical(sort(ro), seq_len(nrow(mat))), "\n")
cat("row order == OLO order:", identical(as.integer(ro), as.integer(get_order(olo_rows[[1]]))), "\n")
d_default <- sum(as.matrix(dist_rows)[cbind(hc_rows$order[-1], hc_rows$order[-nrow(mat)])])
d_olo <- sum(as.matrix(dist_rows)[cbind(as.integer(ro)[-1], as.integer(ro)[-nrow(mat)])])
cat("adjacent-row distance sum: default hclust", round(d_default,1), " OLO", round(d_olo,1), "\n")
cat("column slices:", sapply(co, length), "\n")
# two column slices should separate B from T lineage (planted, real biology)
for (s in seq_along(co)) cat(" slice", s, "lineage counts:", paste(names(table(md$lineage[co[[s]]])), table(md$lineage[co[[s]]]), collapse=" "), "\n")
tab <- table(slice = rep(seq_along(co), sapply(co, length)), lineage = md$lineage[unlist(co)])
print(tab)
# annotation maps to correct samples: recompute from drawn column order
cat("annotation vector in drawn order equals md$lineage[column_order]:", identical(as.character(md$lineage[unlist(co)]), as.character(md$lineage)[unlist(co)]), "\n")
# T-cell marker check: CD3D-like genes (affy 38319_at = CD3D) high in T
g <- c("38319_at"); if (g %in% rownames(X)) { cat("CD3D mean B:", round(mean(X[g, md$lineage=="B-cell"]),2), " T:", round(mean(X[g, md$lineage=="T-cell"]),2), " in top200:", g %in% rownames(mat), "\n") }
# colour at extremes
cat("col_fun(-bounds)==vik[1]:", toupper(substr(col_fun(-bounds),1,7))==toupper(vik[1]), " col_fun(+10) clipped == col_fun(bounds):", col_fun(10)==col_fun(bounds), "\n")
