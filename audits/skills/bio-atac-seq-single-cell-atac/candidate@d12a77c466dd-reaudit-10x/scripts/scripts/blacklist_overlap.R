# how many peaks in each real 10x peak matrix overlap Signac's blacklist_hg38_unified, and does FractionCountsInRegion return finite values
suppressPackageStartupMessages({library(Signac);library(Seurat);library(GenomicRanges)})
P <- file.path(Sys.getenv("ATACDATA"),"10x-multiome")
h <- list(arc=file.path(Sys.getenv("CACHE"),"pbmc_granulocyte_sorted_3k_filtered_feature_bc_matrix.h5"),
          atac2x=file.path(P,"atac2x-pbmc10k/10k_pbmc_ATACv2_nextgem_Chromium_Controller_filtered_peak_bc_matrix.h5"),
          atac1x=file.path(Sys.getenv("ATACDATA"),"scatac/outs/filtered_peak_bc_matrix.h5"))
for (n in names(h)) {
  m <- Read10X_h5(h[[n]]); if (is.list(m)) m <- m[["Peaks"]]
  ca <- CreateChromatinAssay(m, sep=c(":","-"), genome="hg38", min.cells=10, min.features=200)
  o <- CreateSeuratObject(ca, assay="ATAC")
  fr <- suppressWarnings(FractionCountsInRegion(o, assay="ATAC", regions=blacklist_hg38_unified))
  ov <- overlapsAny(granges(ca), blacklist_hg38_unified)
  cat(n,": peaks",nrow(ca),"overlapping blacklist",sum(ov),"; cells",ncol(o),"; ratio range",signif(range(fr,na.rm=TRUE),3),"mean",signif(mean(fr,na.rm=TRUE),3),"n>=0.05",sum(fr>=0.05,na.rm=TRUE),"NaN",sum(is.nan(fr)),"\n")
}
