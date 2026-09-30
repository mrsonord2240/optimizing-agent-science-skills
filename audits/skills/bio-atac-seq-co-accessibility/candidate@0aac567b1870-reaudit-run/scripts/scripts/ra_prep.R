# Re-audit input prep: real public 10x PBMC granulocyte-sorted 3k Multiome ATAC peaks (the cached 5k scATAC is chr1-only), MULTI-chromosome slice (chr1, chr2, chr19 each <= 3 Mb),
# binarized -> pattern-format .mtx (all-ones matrix => writeMM writes 'pattern'), plus a metadata with named header columns.
suppressPackageStartupMessages({library(Seurat);library(Matrix)})
D <- Sys.getenv("ATACDATA"); O <- file.path(Sys.getenv("CO"), "work/reaudit/input"); dir.create(O, recursive=TRUE, showWarnings=FALSE)
m <- Read10X_h5(file.path(Sys.getenv("CO"), "public-cache/pbmc_granulocyte_sorted_3k_filtered_feature_bc_matrix.h5"))$Peaks
m <- m[, Matrix::colSums(m) >= 300]
p <- do.call(rbind, strsplit(sub("^(chr[^:]+):([0-9]+)-([0-9]+)$", "\\1 \\2 \\3", rownames(m)), " "))
keep <- p[,1] %in% c("chr1","chr2","chr19") & as.numeric(p[,3]) <= 4e6
m <- m[keep, ]; m <- m[Matrix::rowSums(m > 0) >= 20, ]
m <- m[, Matrix::colSums(m) > 0]   # drop cells with no reads in the slice (Skill script has no guard for this)
m@x[] <- 1
rownames(m) <- sub("^(chr[^:]+):([0-9]+)-([0-9]+)$", "\\1_\\2_\\3", rownames(m))
m <- as(as(m != 0, "generalMatrix"), "CsparseMatrix")
cat("class", class(m), "dim", dim(m), "\n"); print(table(sub("_.*", "", rownames(m))))
writeMM(m, file.path(O, "peak_matrix.mtx"))
write.table(data.frame(site_name=rownames(m)), file.path(O, "peak_metadata.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
write.table(data.frame(cell=colnames(m)), file.path(O, "cell_metadata.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
cat(readLines(file.path(O, "peak_matrix.mtx"), 1), "\n")
