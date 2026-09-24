# Exact-commit delta check for the two prior P2 findings.
# Mirrors the current SKILL.md inline row-annotation palette construction.
suppressPackageStartupMessages({library(ComplexHeatmap); library(circlize)})

set.seed(6454218)
mat <- matrix(rnorm(36), 6, dimnames = list(paste0("g", 1:6), paste0("s", 1:6)))
mat_scaled <- t(scale(t(mat)))
mat_scaled[is.na(mat_scaled)] <- 0
bounds <- quantile(abs(mat_scaled), 0.99)
gene_info <- data.frame(
  pathway = factor(c("Metabolism", "Signaling", "Immune", "Immune", "Metabolism", "Signaling"),
                   levels = c("Metabolism", "Signaling", "Immune")),
  log2FC = seq(-1, 1, length.out = 6)
)

# Current SKILL.md block: all observed labels receive a color.
pathway_levels <- unique(as.character(gene_info$pathway))
pathway_colors <- setNames(grDevices::hcl.colors(length(pathway_levels), palette = "Dark 3"),
                           pathway_levels)
ha_row <- rowAnnotation(
  Pathway = gene_info$pathway,
  LogFC = anno_barplot(gene_info$log2FC, baseline = 0),
  col = list(Pathway = pathway_colors)
)
stopifnot(identical(ha_row@anno_list$Pathway@color_mapping@levels, pathway_levels))
stopifnot(identical(sort(names(pathway_colors)), sort(pathway_levels)))
stopifnot("Immune" %in% names(pathway_colors))

col_fun <- colorRamp2(c(-bounds, 0, bounds), c("#0072B2", "white", "#D55E00"))
pdf("inline_three_level_annotation.pdf", width = 5, height = 4)
ht_drawn <- draw(Heatmap(mat_scaled, name = "Z", col = col_fun,
                         left_annotation = ha_row, cluster_columns = FALSE))
dev.off()
stopifnot(file.info("inline_three_level_annotation.pdf")$size > 5000)

# The revised text describes the behavior tested in the previous audit.
pdf("top_level_autoprint.pdf", width = 4, height = 4)
Heatmap(mat, name = "value")
dev.off()
stopifnot(file.info("top_level_autoprint.pdf")$size > 5000)
cat("PASS: dynamic colors include Immune; three-level annotation renders; bare top-level call auto-prints\n")
