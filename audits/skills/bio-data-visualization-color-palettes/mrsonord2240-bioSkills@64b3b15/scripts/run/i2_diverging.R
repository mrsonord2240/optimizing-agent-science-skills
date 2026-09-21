# Input 2: diverging LFC heatmap, vik, symmetric bounds, zero must be pure white (SYNTHETIC skewed LFC matrix)
suppressMessages({library(ggplot2);library(scico);library(scales);library(circlize);library(RColorBrewer);library(patchwork)})
set.seed(20260920)
genes <- paste0("G", sprintf("%02d",1:40)); samp <- paste0("S", 1:12)
m <- matrix(rnorm(40*12, 0, 0.6), 40, 12, dimnames=list(genes,samp))
m[1:6, 7:12] <- m[1:6, 7:12] + matrix(rexp(36, 0.6)+1.5, 6, 6)      # strong right skew: a few big up genes
m[7:9, 1:6] <- m[7:9, 1:6] - 1.2                                    # mild down block
m[3,3] <- 0                                                         # exact zero cell to inspect
df <- expand.grid(gene=genes, sample=samp); df$lfc <- as.vector(m)
df$x <- as.integer(df$sample); df$y <- as.integer(df$gene)
write.csv(df[,c("gene","sample","lfc")], "../data/synthetic_skewed_lfc.csv", row.names=FALSE)  # SYNTHETIC
cat("lfc range:", range(df$lfc), " |lfc| 99th pct:", quantile(abs(df$lfc), .99), "\n")
zero_i <- which(df$gene=="G03" & df$sample=="S3"); stopifnot(df$lfc[zero_i]==0)

fill_at_zero <- function(p) { b <- ggplot_build(p)$data[[1]]; toupper(b$fill[zero_i]) }
mk <- function(sc, title) ggplot(df, aes(x, y, fill=lfc)) + geom_tile() + sc + ggtitle(title) + theme_minimal(base_size=8)

# (A) SKILL.md block verbatim: scale_fill_scico(palette='vik', midpoint=0) with no limits
pA <- mk(scale_fill_scico(palette='vik', midpoint=0), "A. SKILL.md: vik, midpoint=0 (no limits)")
# (B) palettes_phd.R block 2 verbatim: symmetric 99% bound with squish
vmax <- quantile(abs(df$lfc), 0.99, na.rm=TRUE)
pB <- mk(scale_fill_scico(palette='vik', midpoint=0, limits=c(-vmax, vmax), oob=scales::squish), "B. example: vik, midpoint=0, limits +-q99, squish")
# (C) skew-naive: vik without midpoint, data range limits
pC <- mk(scale_fill_scico(palette='vik'), "C. vik, default (range-based)")
# (D) Skill's custom diverging: white centre
pD <- mk(scale_fill_gradient2(low='#0072B2', mid='white', high='#D55E00', midpoint=0, limits=c(-vmax,vmax), oob=scales::squish), "D. custom #0072B2/white/#D55E00, symmetric")
cat("\nFill of the EXACT-ZERO cell:\n")
for (n in c("A","B","C","D")) cat(n, get(paste0("p",n)) |> fill_at_zero(), "\n")
cat("vik palette midpoint (scico(255)[128]):", scico(255, palette="vik")[128], "  scico(256, ...) mid pair:", scico(256, palette="vik")[128:129], "\n")
cat("RdBu brewer midpoint:", brewer.pal(11,"RdBu")[6], "\n")
bA <- ggplot_build(pA)$data[[1]]$fill; bB <- ggplot_build(pB)$data[[1]]$fill; bC <- ggplot_build(pC)$data[[1]]$fill
cat("Does A == B fill vectors:", identical(bA,bB), " | number of cells whose fill differs:", sum(bA!=bB), "\n")
# how far is zero from the scale centre in C (default) and what does A do
lims <- ggplot_build(pC)$layout$panel_scales_x  # dummy
cat("C: data range is asymmetric -> centre of scale = ", mean(range(df$lfc)), " not 0\n")
# cells clipped by 99% squish
cat("cells squished by q99 bound:", sum(abs(df$lfc) > vmax), "of", nrow(df), "\n")
# ColorRamp2 pure-white check
col_fun <- colorRamp2(c(-2,0,2), c('#0072B2','white','#D55E00')); cat("colorRamp2 at 0:", col_fun(0), " at -2:", col_fun(-2), "\n")
png("../figs/i2_diverging_heatmaps.png", 1800, 1100, res=150)
print((pA + pB) / (pC + pD) & theme(legend.key.height=unit(.5,"cm")))
dev.off(); cat(file.size("../figs/i2_diverging_heatmaps.png"), "\n")
