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
cat("loaded DLLs with cairo:", grep("airo", names(getLoadedDLLs()), value=TRUE), "
"); f_r <- "i5_raster.pdf"; cairo_pdf(f_r, 7, 9); d1 <- draw(ht, merge_legends = TRUE); dev.off()
ht2 <- Heatmap(z, name = "Z", col = cf, cluster_rows = dend, cluster_columns = TRUE, clustering_method_columns = "ward.D2",
              top_annotation = ha, column_split = 3, show_row_names = FALSE, show_column_names = FALSE, use_raster = FALSE)
f_v <- "i5_vector.pdf"; cairo_pdf(f_v, 7, 9); draw(ht2); dev.off()
cat("PDF sizes: raster_quality=5:", file.size(f_r), " vector cells:", file.size(f_v), "\n")
ht3 <- Heatmap(z, name = "Z", col = cf, cluster_rows = dend, cluster_columns = TRUE, clustering_method_columns = "ward.D2", column_split = 3,
               show_row_names = FALSE, show_column_names = FALSE, use_raster = TRUE, raster_quality = 1)
f_q1 <- "i5_rq1.pdf"; cairo_pdf(f_q1, 7, 9); draw(ht3); dev.off(); cat("raster_quality=1 pdf size:", file.size(f_q1), "\n")
ht4 <- Heatmap(z, name = "Z", col = cf, cluster_rows = dend, cluster_columns = TRUE, clustering_method_columns = "ward.D2", column_split = 3,
               show_row_names = FALSE, show_column_names = FALSE, use_raster = TRUE, raster_quality = 5, raster_device = "CairoPNG")
f_c <- "i5_cairopng.pdf"; cairo_pdf(f_c, 7, 9); draw(ht4); dev.off(); cat("raster_device='CairoPNG' pdf size:", file.size(f_c), "\n")
# default raster trigger
hd <- Heatmap(z, name="Z", show_row_names=FALSE); f_d <- "i5_default.pdf"; pdf(f_d, 7, 9); draw(hd); dev.off()
hs <- Heatmap(z[1:1500,], name="Z", show_row_names=FALSE, cluster_rows=FALSE); f_s <- "i5_default_1500.pdf"; pdf(f_s, 7, 9); draw(hs); dev.off()
cat("default 5000 rows pdf:", file.size(f_d), "  (raster) ; default 1500 rows pdf:", file.size(f_s), " (vector? >> larger per row)\n")
# ---- assertions on module recovery ----
ro <- row_order(d1); co <- column_order(d1)
cat("row order == OLO order:", identical(as.integer(ro), as.integer(get_order(olo[[1]]))), "\n")
cl <- cutree(hc, 5); print(table(cluster = cl, planted = mod))
ari <- function(a,b){ tab <- table(a,b); n <- sum(tab); s <- sum(choose(tab,2)); ra <- sum(choose(rowSums(tab),2)); cb <- sum(choose(colSums(tab),2)); e <- ra*cb/choose(n,2); (s-e)/((ra+cb)/2-e) }
cat("ARI of cutree(k=5) vs planted modules:", round(ari(cl, mod),3), "\n")
cat("column slices (3) sizes:", sapply(co, length), "; each slice single group:", all(sapply(co, function(i) length(unique(grp[i]))==1)), "\n")
