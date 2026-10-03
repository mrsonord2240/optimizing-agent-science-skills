# Re-audit 4 (volcano-and-ma-plots): file-size claims. '17,994 points: 540 KB vector vs 38 KB rasterized (ggrastr)'. Usage: r.sh r4_sizes.R <outdir>
a <- commandArgs(TRUE); out <- a[1]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(DESeq2); library(ggplot2); library(ggrastr)})
dds <- readRDS("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dds_condition.rds")
res <- suppressMessages(suppressWarnings(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm')))
d <- as.data.frame(res); d <- d[!is.na(d$padj), ]; d$y <- -log10(d$padj); cat("points", nrow(d), "\n")
mk <- function(geom) ggplot(d, aes(log2FoldChange, y)) + geom + theme_classic(base_size = 10)
for (nm in c("vector", "ggrastr")) {
  p <- mk(if (nm == "vector") geom_point(alpha = 0.6, size = 1.3) else rasterise(geom_point(alpha = 0.6, size = 1.3), dpi = 300))
  f <- paste0("pts_", nm, ".pdf"); ggsave(f, p, width = 89, height = 90, units = "mm", device = cairo_pdf); cat(sprintf("%-8s %7d B\n", nm, file.size(f)))
}
cat("ggrastr", as.character(packageVersion("ggrastr")), "\n")
write.csv(data.frame(gene = rownames(res), as.data.frame(res)), "airway_shrunk_apeglm.csv", row.names = FALSE)
