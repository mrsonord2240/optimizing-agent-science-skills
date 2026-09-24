# Re-audit input 8: execute the current SKILL.md annotation block with its
# documented three-level pathway metadata, and test the top-level Rscript draw claim.
suppressPackageStartupMessages({library(ComplexHeatmap); library(circlize)})

set.seed(812)
mat <- matrix(rnorm(36), 6, dimnames = list(paste0("g", 1:6), paste0("s", 1:6)))
mat_scaled <- t(scale(t(mat)))
mat_scaled[is.na(mat_scaled)] <- 0
bounds <- quantile(abs(mat_scaled[!is.na(mat_scaled)]), 0.99)
col_fun <- colorRamp2(c(-bounds, 0, bounds), c("#0072B2", "white", "#D55E00"))
metadata <- data.frame(condition = rep(c("Control", "Treatment"), each = 3),
                       batch = rep(c("A", "B", "C"), 2), age = 30:35)
gene_info <- data.frame(pathway = factor(c("Metabolism", "Signaling", "Immune", "Immune", "Metabolism", "Signaling"),
                                         levels = c("Metabolism", "Signaling", "Immune")),
                        log2FC = seq(-1, 1, length.out = 6))

ha_col <- HeatmapAnnotation(
  Condition = metadata$condition, Batch = metadata$batch, Age = anno_barplot(metadata$age),
  col = list(Condition = c(Control = "#56B4E9", Treatment = "#D55E00"),
             Batch = c(A = "#009E73", B = "#0072B2", C = "#CC79A7")))

result <- tryCatch({
  # This is the rowAnnotation colour list currently printed in SKILL.md.
  ha_row <- rowAnnotation(
    Pathway = gene_info$pathway,
    LogFC = anno_barplot(gene_info$log2FC, baseline = 0),
    col = list(Pathway = c(Metabolism = "#8491B4", Signaling = "#91D1C2")))
  ht <- Heatmap(mat_scaled, name = "Z-score", col = col_fun,
                top_annotation = ha_col, left_annotation = ha_row,
                column_split = metadata$condition,
                clustering_method_rows = "ward.D2", clustering_method_columns = "ward.D2",
                show_row_names = FALSE, use_raster = TRUE)
  pdf("inline_annotation_three_levels.pdf", width = 5, height = 5)
  draw(ht, merge_legends = TRUE)
  dev.off()
  "unexpected-success"
}, error = function(e) conditionMessage(e))
cat("three-level inline annotation result:", result, "\n")
stopifnot(grepl("cannot map colors", result))

# A top-level Heatmap expression in Rscript is auto-printed: it creates a real page.
pdf("top_level_bare_heatmap.pdf", width = 4, height = 4)
Heatmap(mat, name = "value")
dev.off()
stopifnot(file.info("top_level_bare_heatmap.pdf")$size > 5000)
cat("PASS: three-level defect reproduced; top-level bare Heatmap produced a nonempty PDF\n")
