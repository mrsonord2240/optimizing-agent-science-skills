has_seurat <- requireNamespace("Seurat", quietly = TRUE)
cat("seurat_installed=", has_seurat, "\n", sep = "")
if (has_seurat) {
  cat("mixscape_lda_exists=", exists("MixscapeLDA", where = asNamespace("Seurat"), inherits = FALSE), "\n", sep = "")
  cat("prep_lda_exists=", exists("PrepLDA", where = asNamespace("Seurat"), inherits = FALSE), "\n", sep = "")
}
