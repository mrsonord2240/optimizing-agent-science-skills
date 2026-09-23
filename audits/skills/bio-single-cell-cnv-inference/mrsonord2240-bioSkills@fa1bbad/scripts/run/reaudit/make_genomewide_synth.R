# RE-AUDIT (2026-09-19): independent genome-wide (all 22 autosomes) real-
# gene synthetic panel, built separately from the fixer's (which left no
# artifacts on disk) to test SCEVAN's documented chromosome-coverage
# requirement and the shipped examples/scevan_calling.R end to end.
suppressMessages(library(copykat))  # for full.anno gene/position table

set.seed(918273)

out_dir <- "/mnt/openscience/audits/bio-single-cell-cnv-inference/run/reaudit/data_genomewide"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

pick_genes <- function(chrom_num, n) {
  sub <- full.anno[full.anno$chromosome_name == as.character(chrom_num) &
                    !is.na(full.anno$start_position), ]
  sub <- sub[order(sub$start_position), ]
  sub <- sub[!duplicated(sub$hgnc_symbol), ]
  sub <- sub[nchar(sub$hgnc_symbol) > 0, ]
  n <- min(n, nrow(sub))
  sub[round(seq(1, nrow(sub), length.out = n)), ]
}

genes_list <- lapply(1:22, pick_genes, n = 40)
genes <- do.call(rbind, genes_list)
genes$gene  <- genes$hgnc_symbol
genes$CHROM <- paste0("chr", genes$chromosome_name)

ref_cells   <- c(paste0("Tcell_", 1:20), paste0("Myeloid_", 1:20))
ref_group   <- c(rep("Tcell", 20), rep("Myeloid", 20))
tumorA      <- paste0("TumorA_", 1:70)   # chr7 gain + chr10 loss
all_cells   <- c(ref_cells, tumorA)
all_groups  <- c(ref_group, rep("malignant_cloneA", 70))

n_genes <- nrow(genes)
n_cells <- length(all_cells)
mat <- matrix(0L, nrow = n_genes, ncol = n_cells,
              dimnames = list(genes$gene, all_cells))

base_mean <- runif(n_genes, 8, 40)
for (j in seq_along(all_cells)) {
  grp <- all_groups[j]
  size_factor <- runif(1, 0.85, 1.15)
  factor <- rep(1.0, n_genes)
  if (grp == "malignant_cloneA") {
    factor[genes$CHROM == "chr7"]  <- 1.6
    factor[genes$CHROM == "chr10"] <- 0.45
  }
  lam <- pmax(0.1, base_mean * factor * size_factor)
  mat[, j] <- rpois(n_genes, lam)
}

write.table(mat, file.path(out_dir, "counts.matrix"), sep = "\t", quote = FALSE,
            col.names = NA)

annot <- data.frame(cell = all_cells,
                     group = ifelse(all_groups %in% c("Tcell", "Myeloid"), all_groups, "Tumor"))
write.table(annot, file.path(out_dir, "cell_annotations.txt"), sep = "\t",
            quote = FALSE, row.names = FALSE, col.names = FALSE)

truth <- data.frame(cell = all_cells, group = all_groups,
                     true_malignant = !(all_groups %in% c("Tcell", "Myeloid")))
write.table(truth, file.path(out_dir, "ground_truth.txt"), sep = "\t",
            quote = FALSE, row.names = FALSE)

cat("wrote genome-wide synthetic panel:", out_dir, "\n")
cat("n_genes:", n_genes, "n_cells:", n_cells, "\n")
cat("genes per chrom:\n"); print(table(genes$CHROM))
