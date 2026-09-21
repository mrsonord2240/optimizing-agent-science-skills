# SKILL.md "Annotation Tracks" block, verbatim, on SYNTHETIC planted data. mat is expected z-scored by the user.
suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize)})
set.seed(11)
ng <- 90; ns <- 18
mat <- matrix(rnorm(ng*ns), ng)
cond <- rep(c("Control","Treatment"), each = 9)
mat[1:30, cond=="Treatment"] <- mat[1:30, cond=="Treatment"] + 2.5
mat[31:60, cond=="Treatment"] <- mat[31:60, cond=="Treatment"] - 2.0
rownames(mat) <- paste0("G", 1:ng); colnames(mat) <- paste0("S", 1:ns)
mat <- t(scale(t(mat)))
metadata <- data.frame(condition = cond, batch = rep(c("A","B","C"), 6), age = round(runif(ns, 25, 75)), row.names = colnames(mat))
run_block <- function(pathways, tag) {
  gene_info <- data.frame(pathway = pathways, log2FC = c(rep(2,30), rep(-2,30), rnorm(30,0,.2)), row.names = rownames(mat))
  res <- tryCatch({
# ---- verbatim from SKILL.md ----
bounds <- quantile(abs(mat[!is.na(mat)]), 0.99)
col_fun <- colorRamp2(c(-bounds, 0, bounds), c('#0072B2', 'white', '#D55E00'))
ha_col <- HeatmapAnnotation(
    Condition = metadata$condition,
    Batch     = metadata$batch,
    Age       = anno_barplot(metadata$age),
    col = list(
        Condition = c(Control = '#56B4E9', Treatment = '#D55E00'),
        Batch     = c(A = '#009E73', B = '#0072B2', C = '#CC79A7')
    ),
    annotation_name_gp = gpar(fontsize = 8)
)
ha_row <- rowAnnotation(
    Pathway = gene_info$pathway,
    LogFC   = anno_barplot(gene_info$log2FC, baseline = 0,
                            gp = gpar(fill = ifelse(gene_info$log2FC > 0,
                                                     '#D55E00', '#0072B2'))),
    col = list(Pathway = c(Metabolism = '#8491B4', Signaling = '#91D1C2'))
)
ht <- Heatmap(mat,
              name = 'Z-score',
              col  = col_fun,
              top_annotation  = ha_col,
              left_annotation = ha_row,
              row_split    = gene_info$pathway,
              column_split = metadata$condition,
              clustering_method_rows    = 'ward.D2',
              clustering_method_columns = 'ward.D2',
              clustering_distance_rows    = 'euclidean',
              clustering_distance_columns = 'euclidean',
              show_row_names = FALSE,
              use_raster = TRUE)          # rasterize cell layer for >2000 rows
png(paste0("i1c_", tag, ".png"), 800, 800, res = 100)
draw(ht, merge_legends = TRUE)            # draw() not bare Heatmap()
dev.off()
# ---- end verbatim ----
  "OK"}, error = function(e) paste("ERROR:", conditionMessage(e)))
  cat(tag, "->", res, "\n")
  if (res == "OK") { d <- draw(ht); print(sapply(row_order(d), length)); print(sapply(column_order(d), length)) }
}
run_block(rep(c("Metabolism","Signaling"), length.out = ng), "two_pathways")
run_block(rep(c("Metabolism","Signaling","Immune"), length.out = ng), "three_pathways_Immune_uncolored")
