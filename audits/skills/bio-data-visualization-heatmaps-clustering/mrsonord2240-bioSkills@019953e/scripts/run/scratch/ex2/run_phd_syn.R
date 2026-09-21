# SYNTHETIC input (planted structure) supplied for heatmap_phd.R, which assumes mat/metadata/gene_info exist.
set.seed(7)
ng <- 120; ns <- 24
mat <- matrix(rnorm(ng*ns, 6, 0.4), ng)
grp <- rep(c("Control","Treatment"), each = 12)
mat[1:40, grp=="Treatment"]  <- mat[1:40, grp=="Treatment"] + 1.5     # up in Treatment
mat[41:80, grp=="Treatment"] <- mat[41:80, grp=="Treatment"] - 1.2    # down in Treatment
rownames(mat) <- paste0("G", 1:ng); colnames(mat) <- paste0("S", 1:ns)
metadata <- data.frame(condition = grp, batch = rep(c("A","B","C"), 8), age = round(runif(ns, 30, 70)), row.names = colnames(mat))
gene_info <- data.frame(pathway = rep(c("Metabolism","Signaling"), length.out = ng), log2FC = c(rep(1.5,40), rep(-1.2,40), rnorm(40,0,.2)), row.names = rownames(mat))
# Reference: ComplexHeatmap 2.18+, circlize 0.4.16+, seriation 1.5+ | Verify API if version differs

# PhD-level annotated heatmap with the four correctness traps encoded:
# (1) ward.D2 NOT ward.D, (2) robust symmetric color bounds, (3) OLO for leaf ordering,
# (4) draw() not bare Heatmap() for non-interactive use.

library(ComplexHeatmap)
library(circlize)
library(seriation)

# 1. INPUT -- mat is features (rows) x samples (cols); metadata is a per-column data.frame
# Assume row z-score is requested (typical bulk RNA-seq case)
mat_scaled <- t(scale(t(mat)))                          # row z-score
mat_scaled[is.na(mat_scaled)] <- 0                      # rows with sd=0 become NaN

# 2. ROBUST SYMMETRIC COLOR BOUNDS -- 1st-99th percentile of |z|
bounds <- quantile(abs(mat_scaled), 0.99, na.rm = TRUE)
col_fun <- colorRamp2(c(-bounds, 0, bounds),
                      c('#0072B2', 'white', '#D55E00'))  # CVD-safe diverging

# 3. CLUSTERING -- ward.D2 not ward.D (Murtagh-Legendre 2014)
d_rows <- dist(mat_scaled, method = 'euclidean')
hc_rows <- hclust(d_rows, method = 'ward.D2')

# 4. OPTIMAL LEAF ORDERING (Bar-Joseph 2001) -- reveals block structure
olo_rows <- seriate(d_rows, method = 'OLO', control = list(hclust = hc_rows))
dend_rows <- as.dendrogram(olo_rows[[1]])

# 5. COLUMN ANNOTATION -- Okabe-Ito categorical palette (Wong 2011)
ha_col <- HeatmapAnnotation(
    Condition = metadata$condition,
    Batch     = metadata$batch,
    Age       = anno_barplot(metadata$age, gp = gpar(fill = '#56B4E9')),
    col = list(
        Condition = c(Control = '#56B4E9', Treatment = '#D55E00'),
        Batch     = c(A = '#009E73', B = '#0072B2', C = '#CC79A7')),
    annotation_name_gp = gpar(fontsize = 8),
    show_legend = TRUE)

# 6. ROW ANNOTATION
ha_row <- rowAnnotation(
    Pathway = gene_info$pathway,
    LogFC   = anno_barplot(gene_info$log2FC, baseline = 0,
                            gp = gpar(fill = ifelse(gene_info$log2FC > 0,
                                                     '#D55E00', '#0072B2'))),
    col = list(Pathway = c(Metabolism = '#8491B4', Signaling = '#91D1C2')))

# 7. ASSEMBLE
ht <- Heatmap(mat_scaled,
              name = 'Z-score',
              col  = col_fun,
              cluster_rows    = dend_rows,                # OLO dendrogram
              cluster_columns = TRUE,
              clustering_method_columns   = 'ward.D2',    # explicit; never 'ward'
              clustering_distance_columns = 'euclidean',
              top_annotation  = ha_col,
              left_annotation = ha_row,
              row_split    = gene_info$pathway,           # grouped row layout
              column_split = metadata$condition,          # grouped column layout
              show_row_names = FALSE,
              show_column_names = TRUE,
              column_names_gp  = gpar(fontsize = 7),
              use_raster = TRUE,                          # raster the cell layer
              raster_quality = 5,                         # publication quality (default 1 is pixelated)
              heatmap_legend_param = list(
                  title_gp = gpar(fontsize = 8, fontface = 'bold'),
                  labels_gp = gpar(fontsize = 7)))

# 8. RENDER -- draw() NOT bare Heatmap() in a script
pdf('heatmap.pdf', width = 7, height = 9)
draw(ht,
     merge_legends = TRUE,
     heatmap_legend_side = 'right',
     annotation_legend_side = 'right',
     padding = unit(c(2, 2, 2, 2), 'mm'))
dev.off()

# 9. EXTRACT CLUSTER ASSIGNMENTS for downstream use
ht_drawn <- draw(ht)
row_order_list <- row_order(ht_drawn)                    # one element per row_split group
column_order_list <- column_order(ht_drawn)
# To get k=4 cuts of the row dendrogram:
row_clusters <- cutree(as.hclust(dend_rows), k = 4)
