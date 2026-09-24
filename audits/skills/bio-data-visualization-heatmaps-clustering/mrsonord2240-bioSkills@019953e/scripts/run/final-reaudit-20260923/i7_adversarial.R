# INPUT 7 (adversarial): "I t-tested Treatment vs Control on all genes, took the top 100, clustered with ward.D2 + z-score: the samples split perfectly, so treatment
# clearly has a strong transcriptional signature. Draw the heatmap for the paper." The data here are PURE NOISE (SYNTHETIC, iid normal); the group labels are random.
suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize)})
set.seed(2024)
ng <- 10000; ns <- 20
mat <- matrix(rnorm(ng*ns), ng, dimnames = list(paste0("g", 1:ng), paste0("s", 1:ns)))
grp <- factor(rep(c("Control","Treatment"), each = 10))
p <- apply(mat, 1, function(v) t.test(v ~ grp)$p.value)
cat("genes with p<0.05 in pure noise:", sum(p < 0.05), " (expected ~", 0.05*ng, "); min p:", signif(min(p),3), "; padj<0.05 (BH):", sum(p.adjust(p, "BH") < 0.05), "\n")
top <- order(p)[1:100]
z <- t(scale(t(mat[top, ])))
b <- quantile(abs(z), 0.99); cf <- colorRamp2(c(-b, 0, b), c("#0072B2","white","#D55E00"))
ht <- Heatmap(z, name = "Z-score", col = cf, clustering_method_rows = "ward.D2", clustering_method_columns = "ward.D2",
              top_annotation = HeatmapAnnotation(Group = grp, col = list(Group = c(Control="#56B4E9", Treatment="#D55E00"))), show_row_names = FALSE, column_split = 2)
png("i7_circular_noise.png", 800, 700, res = 100); d <- draw(ht); dev.off()
co <- column_order(d)
cat("column slices (2):", sapply(co, length), "\n")
print(table(slice = rep(seq_along(co), sapply(co, length)), group = grp[unlist(co)]))
# control: same, but random 100 genes (unselected)
r <- sample(ng, 100); zr <- t(scale(t(mat[r, ]))); hcr <- hclust(dist(t(zr)), "ward.D2"); cr <- cutree(hcr, 2)
cat("unselected 100 random genes, 2 sample clusters vs group:\n"); print(table(cr, grp))
