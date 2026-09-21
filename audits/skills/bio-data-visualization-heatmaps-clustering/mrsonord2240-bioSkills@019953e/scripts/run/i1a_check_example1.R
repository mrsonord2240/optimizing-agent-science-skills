# Assertions on the shipped examples/expression_heatmap.R: source it minus the pdf()/draw() tail, then inspect the object
src <- readLines("scratch/ex1/expression_heatmap.R")
cut <- which(startsWith(src, "pdf("))
suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize)})
eval(parse(text = src[1:(cut-1)]))
pdf(NULL); ht_d <- draw(ht); dev.off()
co <- column_order(ht_d); ro <- row_order(ht_d)
cat("col slices:", names(co), " sizes:", sapply(co,length), "\n")
cat("row slices:", names(ro), " sizes:", sapply(ro,length), "\n")
# independent re-cluster of Control columns with the ComplexHeatmap default (complete/euclidean)
ctrl <- 1:10
hc <- hclust(dist(t(mat[, ctrl])), "complete")
cat("Control column order matches independent hclust(complete):", identical(as.integer(co[["Control"]]), as.integer(hc$order)) || 
    identical(as.integer(co[["Control"]]), rev(as.integer(hc$order))), "\n")
cat("  ComplexHeatmap:", co[["Control"]], "\n  hclust        :", hc$order, "\n")
# each slice contains only its own condition (annotation maps to right samples)
cat("Control slice == samples 1-10:", setequal(co[["Control"]], 1:10), "; Treatment slice == 11-20:", setequal(co[["Treatment"]], 11:20), "\n")
# does the legend 'Z-score' match the data?
cat("row means range (should be ~0 if z-scored): ", round(range(rowMeans(mat)),2), "\n")
cat("row sd range (should be 1 if z-scored):     ", round(range(apply(mat,1,sd)),2), "\n")
cat("fraction of cells beyond +-2 (saturated):    ", round(mean(abs(mat)>2),3), "\n")
cat("col_fun(2)=", col_fun(2), " col_fun(5)=", col_fun(5), " col_fun(0)=", col_fun(0), "\n")
# pathway labels vs planted structure
cat("Pathway 'Immune' rows = genes 1-20, planted treatment-responsive = 1:30, planted immune-correlated = 31:50\n")
cat("mean Treatment-Control diff, genes labelled Immune:", round(mean(rowMeans(mat[gene_info$pathway=='Immune',11:20]) - rowMeans(mat[gene_info$pathway=='Immune',1:10])),2),
    "; labelled Metabolism:", round(mean(rowMeans(mat[gene_info$pathway=='Metabolism',11:20]) - rowMeans(mat[gene_info$pathway=='Metabolism',1:10])),2), "\n")
# The order differs from hclust$order only because ComplexHeatmap reorders the dendrogram (column_dend_reorder). Compare tree topology via cophenetic distances:
dc <- column_dend(ht_d)[["Control"]]
hc2 <- as.hclust(dc)
lab <- colnames(mat)[ctrl]
cp1 <- as.matrix(cophenetic(hc))[lab, lab]
cp2 <- as.matrix(cophenetic(hc2))[lab, lab]
cat("cophenetic identical between independent hclust(complete) and drawn dendrogram:", isTRUE(all.equal(cp1, cp2)), "\n")
# leaf order in the drawn dendrogram equals column_order?
cat("drawn dendrogram leaf order == column_order:", identical(labels(dc), colnames(mat)[co[["Control"]]]), "\n")
