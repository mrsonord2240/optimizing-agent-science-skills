# Build a second synthetic dataset using REAL human gene symbols (needed for
# copyKAT / SCEVAN, which look up chromosome position internally from gene
# symbol rather than taking an explicit gene_order_file like inferCNV does).
# Uses numbat's bundled gtf_hg38 for real symbol/CHROM/position lookups.
# Seeded for reproducibility (also exercises the Skill Veto T3 determinism
# check: run twice, diff the outputs).
suppressMessages(library(copykat))  # for full.anno, the same gene/position
                                     # table copyKAT and SCEVAN key against --
                                     # guarantees these symbols are annotatable

set.seed(20260919)

out_dir <- "/mnt/openscience/audits/bio-single-cell-cnv-inference/data_realgenes"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

pick_genes <- function(chrom_num, n) {
  sub <- full.anno[full.anno$chromosome_name == as.character(chrom_num) &
                    !is.na(full.anno$start_position), ]
  sub <- sub[order(sub$start_position), ]
  sub <- sub[!duplicated(sub$hgnc_symbol), ]
  sub <- sub[nchar(sub$hgnc_symbol) > 0, ]
  sub[round(seq(1, nrow(sub), length.out = n)), ]
}

g_chr1  <- pick_genes(1, 350)
g_chr7  <- pick_genes(7, 350)
g_chr10 <- pick_genes(10, 350)
genes <- rbind(g_chr1, g_chr7, g_chr10)
genes$gene  <- genes$hgnc_symbol
genes$CHROM <- paste0("chr", genes$chromosome_name)
genes$gene_start <- genes$start_position
genes$gene_end   <- genes$end_position

ref_cells   <- c(paste0("Tcell_", 1:20), paste0("Myeloid_", 1:20))
ref_group   <- c(rep("Tcell", 20), rep("Myeloid", 20))
tumorA      <- paste0("TumorA_", 1:70)   # chr7 gain + chr10 loss
tumorB      <- paste0("TumorB_", 1:40)   # chr7 gain only
all_cells   <- c(ref_cells, tumorA, tumorB)
all_groups  <- c(ref_group, rep("malignant_cloneA", 70), rep("malignant_cloneB", 40))

n_genes <- nrow(genes)
n_cells <- length(all_cells)
mat <- matrix(0L, nrow = n_genes, ncol = n_cells,
              dimnames = list(genes$gene, all_cells))

base_mean <- runif(n_genes, 8, 40)
for (j in seq_along(all_cells)) {
  grp <- all_groups[j]
  size_factor <- runif(1, 0.85, 1.15)
  factor <- rep(1.0, n_genes)
  if (grp %in% c("malignant_cloneA", "malignant_cloneB")) {
    factor[genes$CHROM == "chr7"] <- 1.6
  }
  if (grp == "malignant_cloneA") {
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

gene_order <- data.frame(gene = genes$gene, chr = genes$CHROM,
                          start = genes$gene_start, stop = genes$gene_end)
write.table(gene_order, file.path(out_dir, "gene_ordering.txt"), sep = "\t",
            quote = FALSE, row.names = FALSE, col.names = FALSE)

truth <- data.frame(cell = all_cells, group = all_groups,
                     true_malignant = !(all_groups %in% c("Tcell", "Myeloid")),
                     true_clone = all_groups)
write.table(truth, file.path(out_dir, "ground_truth_clones.txt"), sep = "\t",
            quote = FALSE, row.names = FALSE)

cat("wrote real-gene synthetic dataset:", out_dir, "\n")
cat("n_genes:", n_genes, "n_cells:", n_cells, "\n")
cat("genes per chrom:\n"); print(table(genes$CHROM))
