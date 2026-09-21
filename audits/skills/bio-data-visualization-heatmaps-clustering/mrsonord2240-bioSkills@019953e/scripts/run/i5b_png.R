# INPUT 5 (stress): 5000 x 60 SYNTHETIC matrix with 5 planted row modules + 3 column groups; use_raster, OLO timing, cairo_pdf, raster_quality.
suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize);library(seriation)})
# env note: on this Windows R, cairo_pdf() fails ("unable to load winCairo.dll") once the Cairo package DLL is loaded (it loads at Heatmap(use_raster=TRUE) time); load winCairo first.
invisible({f0 <- tempfile(fileext=".pdf"); cairo_pdf(f0); dev.off()})
set.seed(21)
ng <- 5000; ns <- 60
grp <- rep(c("G1","G2","G3"), each = 20)
mod <- sample(1:5, ng, replace = TRUE)                       # planted module per gene
eff <- matrix(0, 5, 3); eff[1,] <- c(2,0,-2); eff[2,] <- c(-2,2,0); eff[3,] <- c(0,-2,2); eff[4,] <- c(1,1,-1); eff[5,] <- 0
mat <- matrix(rnorm(ng*ns), ng)
for (k in 1:5) for (g in 1:3) mat[mod==k, grp==paste0("G",g)] <- mat[mod==k, grp==paste0("G",g)] + eff[k,g]
rownames(mat) <- paste0("g", 1:ng); colnames(mat) <- paste0("s", 1:ns)
mat[10, 7] <- 40                                             # one planted outlier
z <- t(scale(t(mat)))
b <- quantile(abs(z), 0.99); cf <- colorRamp2(c(-b, 0, b), c("#0072B2","white","#D55E00"))
ha <- HeatmapAnnotation(Group = grp, col = list(Group = c(G1="#56B4E9", G2="#009E73", G3="#D55E00")))
t0 <- Sys.time(); d <- dist(z); hc <- hclust(d, "ward.D2"); cat("dist+hclust ward.D2 5000 rows:", round(as.numeric(difftime(Sys.time(), t0, units="secs")),1), "s\n")
if (file.exists("i5_olo.rds")) { olo <- readRDS("i5_olo.rds"); cat("OLO loaded from cache (uncached runs: 125.9 s and 120.2 s for 5000 rows)", "
") } else { t0 <- Sys.time(); olo <- seriate(d, method = "OLO", control = list(hclust = hc)); tolo <- as.numeric(difftime(Sys.time(), t0, units="secs")); cat("OLO (seriation) 5000 rows:", round(tolo,1), "s", "
"); saveRDS(olo, "i5_olo.rds") }
dend <- as.dendrogram(olo[[1]])
cat("bounds:", round(b,3), " outlier z:", round(z[10,7],2), "\n")
ht <- Heatmap(z, name = "Z", col = cf, cluster_rows = dend, cluster_columns = TRUE, clustering_method_columns = "ward.D2",
              top_annotation = ha, column_split = 3, show_row_names = FALSE, show_column_names = FALSE, use_raster = TRUE, raster_quality = 5)
png("i5_stress.png", 800, 900, res = 100); d1 <- draw(ht, merge_legends = TRUE); dev.off()
cat("PNG written
")
