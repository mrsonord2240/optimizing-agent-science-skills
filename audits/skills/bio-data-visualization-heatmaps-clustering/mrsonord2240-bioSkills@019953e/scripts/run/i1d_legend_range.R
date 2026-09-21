suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize)})
set.seed(1); m <- matrix(rnorm(400), 20)
cf <- colorRamp2(c(-2.5,0,2.5), c("blue","white","red"))
cat("breaks:", attr(cf,"breaks"), "\n")
ht <- Heatmap(m, name="z", col=cf)
cm <- ht@matrix_color_mapping
cat("legend 'at' computed by ComplexHeatmap:", cm@levels, "\n")
cf2 <- colorRamp2(c(-4,0,4), c("blue","white","red"))
cat("range(m):", range(m), "\n")
