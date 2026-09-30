# Signac CallPeaks (MACS3) per cluster + scDblFinder (amulet(), and synthetic-doublet ATAC mode) on real PBMC 5k chr1 slice
suppressPackageStartupMessages({library(Signac);library(Seurat);library(magrittr);library(GenomicRanges);library(EnsDb.Hsapiens.v86);library(scDblFinder);library(SingleCellExperiment)})
D <- Sys.getenv("ATACDATA"); SCA <- Sys.getenv("SCA"); setwd(file.path(SCA,"work")); set.seed(1)
counts <- Read10X_h5(file.path(D,"scatac/outs/filtered_peak_bc_matrix.h5"))
ann <- GetGRangesFromEnsDb(EnsDb.Hsapiens.v86); seqlevelsStyle(ann) <- "UCSC"; genome(ann) <- "hg38"
frag <- file.path(D,"scatac/outs/fragments.tsv.gz")
ca <- CreateChromatinAssay(counts, sep=c(":","-"), genome="hg38", fragments=frag, annotation=ann, min.cells=10, min.features=200)
obj <- CreateSeuratObject(ca, assay="ATAC"); cat("cells", ncol(obj), "\n")
obj <- RunTFIDF(obj) %>% FindTopFeatures(min.cutoff='q0') %>% RunSVD()
obj <- FindNeighbors(obj, reduction='lsi', dims=2:30) %>% FindClusters(algorithm=4, resolution=0.5, verbose=FALSE)
cat("clusters", table(obj$seurat_clusters), "\n")
mac <- Sys.getenv("MACS3"); cat("macs3", mac, "\n")
peaks <- CallPeaks(obj, group.by='seurat_clusters', macs2.path=mac, cleanup=FALSE, format='BED', shift=-75, extsize=150, additional.args='-p 0.01')
cat("CallPeaks ->", class(peaks), length(peaks), "\n"); print(head(peaks,3)); print(table(peaks$peak_called_in)[1:min(6,length(table(peaks$peak_called_in)))])
cat("peak chr", unique(as.character(seqnames(peaks))), " width median", median(width(peaks)), "\n")
# overlap with 10x peaks
tx <- rtracklayer::import(file.path(D,"scatac/outs/peaks.bed")); tx <- tx[seqnames(tx)=="chr1" & end(tx)<=30e6]
cat("fraction of CallPeaks overlapping 10x peaks (chr1 30Mb):", round(mean(overlapsAny(peaks, tx)),3), " (n peaks in range", sum(end(peaks)<=30e6), ")\n")
# scDblFinder amulet() on fragments
bc <- colnames(obj)[1:min(1500, ncol(obj))]
am <- tryCatch(amulet(frag, regionsToExclude=GRanges(c("chrM","chrX","chrY"), IRanges(1,5e8))), error=function(e){cat("amulet FAILED:", conditionMessage(e),"\n"); NULL})
if(!is.null(am)){ cat("amulet result dim", dim(am), "cols", colnames(am), "\n"); print(head(am,3)); cat("n flagged q<0.05:", sum(am$q.value<0.05,na.rm=TRUE), "of", nrow(am), "\n")
  saveRDS(am, "amulet.rds") }
# synthetic-doublet ATAC mode
sce <- SingleCellExperiment(list(counts=GetAssayData(obj,assay="ATAC",layer="counts")))
res <- tryCatch(scDblFinder(sce, aggregateFeatures=TRUE, nfeatures=25, processing="normFeatures"), error=function(e){cat("scDblFinder FAILED:", conditionMessage(e),"\n"); NULL})
if(!is.null(res)){ cat("scDblFinder classes", table(res$scDblFinder.class), " score range", round(range(res$scDblFinder.score),3), "\n")
  cat("cor(score, log depth)", round(cor(res$scDblFinder.score, log10(colSums(counts(sce)))),3), "\n") }
