# Independent check of the ARC blacklist-ratio approximation: on ATAC 1.0.1 (which has the official
# blacklist_region_fragments column) compare official ratio vs the peak-matrix FractionCountsInRegion used for ARC.
suppressPackageStartupMessages({library(Signac);library(Seurat);library(GenomicRanges)})
D <- file.path(Sys.getenv("ATACDATA"),"scatac/outs")
cnt <- Read10X_h5(file.path(D,"filtered_peak_bc_matrix.h5"))
md <- read.csv(file.path(D,"singlecell.csv"),row.names=1)[colnames(cnt),]
ca <- CreateChromatinAssay(cnt, sep=c(":","-"), genome="hg38", min.cells=0, min.features=0)
o <- CreateSeuratObject(ca, assay="ATAC", meta.data=md)
approx <- FractionCountsInRegion(o, assay="ATAC", regions=blacklist_hg38_unified)
official <- md$blacklist_region_fragments/md$peak_region_fragments
cat("cells",ncol(o),"\n")
cat("official ratio range",signif(range(official),3),"median",signif(median(official),3),"frac>=0.05",mean(official>=0.05),"\n")
cat("approx   ratio range",signif(range(approx),3),"median",signif(median(approx),3),"frac>=0.05",mean(approx>=0.05),"\n")
cat("spearman",round(cor(official,approx,method="spearman"),3),"pearson",round(cor(official,approx),3),"\n")
cat("cells flagged (>=0.05) by one but not the other:",sum((official>=0.05)!=(approx>=0.05)),"\n")
cat("n peaks overlapping blacklist:",sum(overlapsAny(granges(ca),blacklist_hg38_unified)),"of",nrow(ca),"\n")
