# INPUT 4 (Variant B): REAL airway RNA-seq (Himes 2014; 8 samples, 4 cell lines x dex). Sample-correlation QC heatmap, then
# expression z-score heatmap + logFC/padj heatmap concatenated with shared row order (usage-guide prompts; SKILL.md has no code for either).
suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize);library(airway);library(DESeq2);library(scico);library(SummarizedExperiment)})
data(airway); dds <- DESeqDataSet(airway, ~ cell + dex); dds <- dds[rowSums(counts(dds)) >= 10, ]
vsd <- assay(vst(dds, blind = TRUE)); md <- as.data.frame(colData(airway))
cat("vst matrix:", dim(vsd), "\n")
top <- order(apply(vsd, 1, var), decreasing = TRUE)[1:500]
cm <- cor(vsd[top, ], method = "pearson")
cat("cor symmetric:", isSymmetric(cm), " diag==1:", all(abs(diag(cm)-1) < 1e-12), " range off-diag:", round(range(cm[upper.tri(cm)]), 4), "\n")
ha <- HeatmapAnnotation(Cell = md$cell, Dex = md$dex, col = list(Cell = c(N61311="#56B4E9", N052611="#009E73", N080611="#CC79A7", N061011="#F0E442"), Dex = c(untrt="#999999", trt="#D55E00")))
ha_r <- rowAnnotation(Cell = md$cell, Dex = md$dex, col = list(Cell = c(N61311="#56B4E9", N052611="#009E73", N080611="#CC79A7", N061011="#F0E442"), Dex = c(untrt="#999999", trt="#D55E00")), show_legend = FALSE)
rng <- range(cm[upper.tri(cm)])
cf <- colorRamp2(seq(rng[1], 1, length.out = 9), rev(scico(9, palette = "batlow")))   # sequential, limits = observed range (not 0..1)
dcor <- as.dist(1 - cm); hc <- hclust(dcor, "ward.D2")
ht_q <- Heatmap(cm, name = "Pearson r", col = cf, cluster_rows = hc, cluster_columns = hc, top_annotation = ha, left_annotation = ha_r,
                column_names_gp = gpar(fontsize = 8), row_names_gp = gpar(fontsize = 8))
png("i4_sample_cor.png", 800, 700, res = 110); dq <- draw(ht_q); dev.off()
oc <- row_order(dq); cc <- column_order(dq)
cat("row order == column order (symmetric):", identical(as.integer(oc), as.integer(cc)), " == hclust order:", identical(as.integer(oc), as.integer(hc$order)) || identical(as.integer(oc), rev(as.integer(hc$order))), "\n")
cat("drawn order (sample, cell, dex):\n"); print(md[oc, c("cell","dex")])
# do pairs of the same cell line sit adjacent?
o <- md$cell[oc]; cat("same-cell-line adjacent pairs in order:", sum(o[-1] == o[-length(o)]), "of 7 adjacent steps\n")
# --------- concatenation: expression z (top 40 DE genes) + log2FC / -log10 padj columns, shared row order ---------
res <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv"); rownames(res) <- res$gene
cat("public results columns:", colnames(res), " n=", nrow(res), "\n")
sig <- res[!is.na(res$padj), ]; sig <- sig[order(sig$padj), ][1:40, ]
g <- intersect(rownames(sig), rownames(vsd)); cat("top-40 DE genes present in vst:", length(g), "\n")
zz <- t(scale(t(vsd[g, ]))); b <- quantile(abs(zz), 0.99)
cf2 <- colorRamp2(c(-b, 0, b), scico(3, palette = "vik")[c(1,2,3)])
h1 <- Heatmap(zz, name = "Z-score", col = cf2, top_annotation = HeatmapAnnotation(Dex = md$dex, Cell = md$cell, col = list(Dex = c(untrt="#999999", trt="#D55E00"), Cell = c(N61311="#56B4E9", N052611="#009E73", N080611="#CC79A7", N061011="#F0E442"))),
              clustering_method_rows = "ward.D2", column_split = md$dex, cluster_column_slices = FALSE, show_row_names = TRUE, row_names_gp = gpar(fontsize = 6), column_names_gp = gpar(fontsize = 8))
lfc <- as.matrix(sig[g, "log2FoldChange", drop = FALSE]); colnames(lfc) <- "log2FC"
fmax <- max(abs(lfc)); h2 <- Heatmap(lfc, name = "log2FC", col = colorRamp2(c(-fmax, 0, fmax), scico(3, palette = "vik")), cluster_rows = FALSE, width = unit(8, "mm"), show_row_names = FALSE)
png("i4_concat.png", 900, 800, res = 110); dc <- draw(h1 + h2, merge_legends = TRUE); dev.off()
ro <- row_order(dc)                          # list per heatmap? for concatenation: row_order returns the order (shared)
ro <- if (is.list(ro)) unlist(ro) else ro
cat("row order is a permutation of 40 genes:", identical(sort(as.integer(ro)), 1:40), "\n")
# direction check: genes with positive log2FC must have higher z in trt than untrt
dz <- rowMeans(zz[, md$dex=="trt"]) - rowMeans(zz[, md$dex=="untrt"])
cat("sign(log2FC) == sign(mean z trt - untrt) for all 40:", all(sign(lfc[,1]) == sign(dz)), "\n")
# lfc rows in same order as expression rows?
cat("h2 rows aligned to h1 rows (same rownames):", identical(rownames(lfc), rownames(zz)), "\n")
