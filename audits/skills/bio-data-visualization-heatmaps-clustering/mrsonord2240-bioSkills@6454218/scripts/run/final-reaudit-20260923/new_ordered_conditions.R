# Re-audit input 9: verify the ordered-condition advice only preserves order
# when cluster_columns is disabled, including a column_split group layout.
suppressPackageStartupMessages(library(ComplexHeatmap))

mat <- rbind(
  seq(0, 7), rev(seq(0, 7)), c(0, 0, 1, 2, 4, 5, 6, 7), c(7, 6, 5, 4, 2, 1, 0, 0))
colnames(mat) <- paste0(c(0, 1, 2, 4, 8, 12, 24, 48), "h")
groups <- factor(c("early", "early", "early", "early", "late", "late", "late", "late"),
                 levels = c("early", "late"))

ht_keep <- Heatmap(mat, cluster_columns = FALSE, column_split = groups, show_row_names = FALSE)
pdf("ordered_conditions.pdf", width = 5, height = 4)
d_keep <- draw(ht_keep)
dev.off()
kept <- unlist(column_order(d_keep), use.names = FALSE)
cat("kept order:", paste(colnames(mat)[kept], collapse = ","), "\n")
stopifnot(identical(as.integer(kept), seq_len(ncol(mat))))
cat("PASS: cluster_columns=FALSE plus column_split preserves input order\n")
