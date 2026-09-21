# diagnostic run of heatmap_phd.R with row_split removed (verbatim otherwise) + assertions; SYNTHETIC input from preamble_syn.R
src <- readLines("phd_nosplit.R")
src[startsWith(src, "pdf(")] <- "png('phd_nosplit.png', width = 700, height = 900, res = 100)"
eval(parse(text = paste(readLines("preamble_syn.R"), collapse="\n")))
eval(parse(text = paste(src, collapse="\n")))
cat("--- assertions ---\n")
cat("bounds (99th pct |z|):", round(bounds,3), " col_fun(-bounds)=", col_fun(-bounds), " col_fun(0)=", col_fun(0), "\n")
cat("row means ~0:", all(abs(rowMeans(mat_scaled))<1e-9), "; row sd 1:", all(abs(apply(mat_scaled,1,sd)-1)<1e-9), "\n")
ro <- unlist(row_order_list)
olo_ord <- as.integer(seriation::get_order(olo_rows[[1]]))
cat("row_order(ht) == OLO order:", identical(as.integer(ro), olo_ord), "\n")
cat("labels of dendrogram == OLO order:", identical(labels(dend_rows), rownames(mat_scaled)[olo_ord]), "\n")
adj <- function(o) { d <- as.matrix(d_rows); sum(d[cbind(o[-length(o)], o[-1])]) }
cat("adjacent-distance sum: default hclust", round(adj(hc_rows$order),1), " OLO", round(adj(olo_ord),1), "\n")
cat("cutree names align with rownames:", identical(names(row_clusters), rownames(mat_scaled)), "\n")
truth <- c(rep("up",40), rep("down",40), rep("null",40))
print(table(cluster = row_clusters, truth = truth))
co <- column_order(ht_drawn); cat("column slices:", names(co), sapply(co, length), "\n")
cat("Control slice contains only Control samples:", all(metadata$condition[co[["Control"]]]=="Control"), "\n")
